// Provision the flat object layout (project, series collections, inventory, SOP, specimens, steps)
// from generated/<stem>/demo_series.json. Runs in a signed-in ELN tab (session cookie, no credentials).
//
//   const r = await provisionDemo(DEMO, SOP_TEXT, { dryRun: true });
//
// Idempotent: existing objects (by identifier) are skipped, never modified. Properties that are not
// assigned to the type on the instance are dropped and reported (e.g. standard props not yet synced).

async function provisionDemo(DEMO, SOP_TEXT, { dryRun = true } = {}) {
  const tok = (document.cookie.match(/openbis=([^;]+)/) || [])[1];
  const call = async (method, ...params) => {
    const r = await (await fetch("/openbis/openbis/rmi-application-server-v3.json", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ method, params: [tok, ...params], id: "1", jsonrpc: "2.0" }),
    })).json();
    if (r.error) throw new Error(method + ": " + JSON.stringify(r.error));
    return r.result;
  };
  const T = (t, o = {}) => ({ "@type": t, ...o });
  const SID = (i) => T("as.dto.sample.id.SampleIdentifier", { identifier: i });
  const EID = (i) => T("as.dto.experiment.id.ExperimentIdentifier", { identifier: i });
  const PID = (i) => T("as.dto.project.id.ProjectIdentifier", { identifier: i });
  const SPID = (c) => T("as.dto.space.id.SpacePermId", { permId: c });
  const TID = (c, kind) => T("as.dto.entitytype.id.EntityTypePermId", { permId: c, entityKind: kind });
  const report = { created: [], skipped: [], droppedProps: [] };

  // assigned property codes per sample type (to drop unknown props instead of failing)
  const sts = await call("searchSampleTypes", T("as.dto.sample.search.SampleTypeSearchCriteria"),
    T("as.dto.sample.fetchoptions.SampleTypeFetchOptions", { propertyAssignments: T("as.dto.property.fetchoptions.PropertyAssignmentFetchOptions", { propertyType: T("as.dto.property.fetchoptions.PropertyTypeFetchOptions") }) }));
  const ids = {}; (function w(o) { if (o && typeof o === "object") { if (o["@id"] !== undefined) ids[o["@id"]] = o; for (const k in o) w(o[k]); } })(sts);
  const assigned = Object.fromEntries(sts.objects.map((s) => [s.code, new Set((s.propertyAssignments || []).map((a) => (typeof a.propertyType === "number" ? ids[a.propertyType] : a.propertyType).code))]));
  const clean = (type, code, props) => {
    const out = {};
    for (const [k, v] of Object.entries(props || {})) {
      if (v === null || v === undefined) continue;
      if (assigned[type] && assigned[type].has(k)) out[k] = String(v); else report.droppedProps.push(`${code}: ${k}`);
    }
    return out;
  };
  const exists = async (kind, identifiers) => {
    if (!identifiers.length) return new Set();
    const r = kind === "sample"
      ? await call("getSamples", identifiers.map(SID), T("as.dto.sample.fetchoptions.SampleFetchOptions"))
      : kind === "experiment"
        ? await call("getExperiments", identifiers.map(EID), T("as.dto.experiment.fetchoptions.ExperimentFetchOptions"))
        : await call("getProjects", identifiers.map(PID), T("as.dto.project.fetchoptions.ProjectFetchOptions"));
    return new Set(Object.keys(r));
  };

  const projId = `/${DEMO.space}/${DEMO.project.code}`;
  // 1 project
  if ((await exists("project", [projId])).size) report.skipped.push(projId);
  else {
    report.created.push(projId);
    if (!dryRun) await call("createProjects", [T("as.dto.project.create.ProjectCreation", { spaceId: SPID(DEMO.space), code: DEMO.project.code, description: DEMO.project.description })]);
  }
  // 2 collections
  const colIds = DEMO.collections.map((c) => `${projId}/${c.code}`);
  const colHave = await exists("experiment", colIds);
  const colNew = DEMO.collections.filter((c, i) => !colHave.has(colIds[i]));
  colIds.filter((i) => colHave.has(i)).forEach((i) => report.skipped.push(i));
  colNew.forEach((c) => report.created.push(`${projId}/${c.code}`));
  if (!dryRun && colNew.length) await call("createExperiments", colNew.map((c) => T("as.dto.experiment.create.ExperimentCreation", {
    typeId: TID("COLLECTION", "EXPERIMENT"), projectId: PID(projId), code: c.code,
    properties: { "$NAME": c.name, "$DEFAULT_OBJECT_TYPE": c.default_object_type, "$DEFAULT_COLLECTION_VIEW": "LIST_VIEW" },
  })));

  // 3 samples: inventory, SOP, specimens (pass 1) and steps (pass 2)
  const inv = Object.fromEntries(DEMO.inventory.map((x) => {
    const [, space, project] = x.collection.split("/");
    return [x.key, { ...x, identifier: `/${space}/${project}/${x.code}`, space, project }];
  }));
  const pass1 = [];
  for (const x of Object.values(inv)) pass1.push({ identifier: x.identifier, c: T("as.dto.sample.create.SampleCreation", {
    typeId: TID(x.type, "SAMPLE"), spaceId: SPID(x.space), projectId: PID(`/${x.space}/${x.project}`), experimentId: EID(x.collection),
    code: x.code, properties: clean(x.type, x.code, x.props) }) });
  const sopType = DEMO.sop.type || "GENERAL_PROTOCOL";
  const sopProps = Object.fromEntries(Object.entries(DEMO.sop.props).map(([k, v]) => [k, v === "@sop_text" ? SOP_TEXT : v]));
  pass1.push({ identifier: `${projId}/${DEMO.sop.code}`, c: T("as.dto.sample.create.SampleCreation", {
    typeId: TID(sopType, "SAMPLE"), spaceId: SPID(DEMO.space), projectId: PID(projId), code: DEMO.sop.code, properties: clean(sopType, DEMO.sop.code, sopProps) }) });
  const SPEC_TYPE = DEMO.collections[0].default_object_type;
  for (const s of DEMO.specimens) pass1.push({ identifier: `${projId}/${s.code}`, c: T("as.dto.sample.create.SampleCreation", {
    typeId: TID(SPEC_TYPE, "SAMPLE"), spaceId: SPID(DEMO.space), projectId: PID(projId), experimentId: EID(`${projId}/${s.collection}`),
    code: s.code, properties: clean(SPEC_TYPE, s.code, { "$NAME": s.code, NOTES: "DEMO - fictitious values//DEMO - fiktive Werte", ...s.props }) }) });

  const STEP = {
    SCAN: { type: "EXPERIMENTAL_STEP", name: "03-04 3D scan & weld analysis", desc: "ZEISS GOM ATOS 5 scan; weld analysis in GOM software, rating stored on the specimen (section 04)//3D-Scan mit ZEISS GOM ATOS 5; Nahtanalyse in der GOM-Software, Bewertung an der Probe (Sektion 04)" },
    TEST: { type: "EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST", name: "07-11 Cyclic fatigue test", desc: null },
    FRACTURE: { type: "EXPERIMENTAL_STEP", name: "12 Fracture surface analysis", desc: "Macroscopic and light-microscopic fracture surface analysis//Makroskopische und lichtmikroskopische Bruchflächenanalyse" },
  };
  const pass2 = [];
  for (const s of DEMO.specimens) for (const [kind, st] of Object.entries(s.steps || {})) {
    if (!st) continue;
    const code = `${s.code}-${kind}`;
    const props = { "$NAME": `${s.code} · ${STEP[kind].name}`, START_DATE: st.start, FINISHED_FLAG: st.done ? "true" : "false", NOTES: "DEMO - fictitious values//DEMO - fiktive Werte",
      ...(STEP[kind].desc ? { "EXPERIMENTAL_STEP.EXPERIMENTAL_DESCRIPTION": STEP[kind].desc } : {}), ...(st.props || {}) };
    pass2.push({ identifier: `${projId}/${code}`, c: T("as.dto.sample.create.SampleCreation", {
      typeId: TID(STEP[kind].type, "SAMPLE"), spaceId: SPID(DEMO.space), projectId: PID(projId), experimentId: EID(`${projId}/${s.collection}`),
      code, properties: clean(STEP[kind].type, code, props),
      parentIds: [SID(`${projId}/${s.code}`), ...DEMO.step_parents[kind].map((k) => SID(inv[k].identifier))] }) });
  }
  for (const pass of [pass1, pass2]) {
    const have = await exists("sample", pass.map((p) => p.identifier));
    const todo = pass.filter((p) => !have.has(p.identifier));
    pass.filter((p) => have.has(p.identifier)).forEach((p) => report.skipped.push(p.identifier));
    todo.forEach((p) => report.created.push(p.identifier));
    if (!dryRun && todo.length) await call("createSamples", todo.map((p) => p.c));
  }
  return { dryRun, ...report };
}
