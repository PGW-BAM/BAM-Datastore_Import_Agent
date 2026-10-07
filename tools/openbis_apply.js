// Idempotent masterdata apply for openBIS 20.10 (V3 JSON-RPC), run inside a signed-in ELN tab.
// No credentials involved: the session token is taken from the browser cookie of the user's own login.
//
//   const report = await applySpec(SPEC, { dryRun: true });   // plan only
//   const report = await applySpec(SPEC, { dryRun: false });  // create what is missing
//
// SPEC = output of tools/export_spec.py. The function only CREATES (vocabularies, terms, property
// types, object types, missing assignments). It never deletes or changes existing definitions;
// differences are reported as conflicts for a human/admin to resolve.

async function applySpec(SPEC, { dryRun = true } = {}) {
  const tok = (document.cookie.match(/openbis=([^;]+)/) || [])[1];
  if (!tok) throw new Error("No openBIS session cookie - sign in first");
  const call = async (method, ...params) => {
    const r = await (await fetch("/openbis/openbis/rmi-application-server-v3.json", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ method, params: [tok, ...params], id: "1", jsonrpc: "2.0" }),
    })).json();
    if (r.error) throw new Error(method + ": " + JSON.stringify(r.error));
    return r.result;
  };
  const T = (t, o = {}) => ({ "@type": t, ...o });
  const VID = (c) => T("as.dto.vocabulary.id.VocabularyPermId", { permId: c });
  const PTID = (c) => T("as.dto.property.id.PropertyTypePermId", { permId: c });
  const STID = (c) => T("as.dto.entitytype.id.EntityTypePermId", { permId: c, entityKind: "SAMPLE" });
  const dt = (d) => (d === "OBJECT" ? "SAMPLE" : d);

  // ---- current state -------------------------------------------------------------------
  const vocs = await call("searchVocabularies", T("as.dto.vocabulary.search.VocabularySearchCriteria"),
    T("as.dto.vocabulary.fetchoptions.VocabularyFetchOptions", { terms: T("as.dto.vocabulary.fetchoptions.VocabularyTermFetchOptions") }));
  const liveVoc = Object.fromEntries(vocs.objects.map((v) => [v.code, new Set((v.terms || []).map((t) => t.code))]));
  const pts = await call("searchPropertyTypes", T("as.dto.property.search.PropertyTypeSearchCriteria"),
    T("as.dto.property.fetchoptions.PropertyTypeFetchOptions"));
  const livePT = Object.fromEntries(pts.objects.map((p) => [p.code, p.dataType]));
  const sts = await call("searchSampleTypes", T("as.dto.sample.search.SampleTypeSearchCriteria"),
    T("as.dto.sample.fetchoptions.SampleTypeFetchOptions", { propertyAssignments: T("as.dto.property.fetchoptions.PropertyAssignmentFetchOptions", { propertyType: T("as.dto.property.fetchoptions.PropertyTypeFetchOptions") }) }));
  const ids = {}; (function w(o) { if (o && typeof o === "object") { if (o["@id"] !== undefined) ids[o["@id"]] = o; for (const k in o) w(o[k]); } })(sts);
  const liveST = Object.fromEntries(sts.objects.map((s) => [s.code, new Set((s.propertyAssignments || []).map((a) => (typeof a.propertyType === "number" ? ids[a.propertyType] : a.propertyType).code))]));

  // ---- plan ----------------------------------------------------------------------------
  const plan = { vocabularies: [], terms: [], propertyTypes: [], sampleTypes: [], assignments: [] };
  const report = { skipped: [], conflicts: [], existing: [] };
  const willVoc = new Set(Object.keys(liveVoc));

  for (const v of SPEC.vocabularies) {
    if (liveVoc[v.code]) { report.existing.push("vocabulary " + v.code); continue; }
    plan.vocabularies.push(T("as.dto.vocabulary.create.VocabularyCreation", {
      code: v.code, description: v.description,
      terms: v.terms.map((t) => T("as.dto.vocabulary.create.VocabularyTermCreation", { code: t.code, label: t.label, description: t.description })),
    }));
    willVoc.add(v.code);
  }
  for (const e of SPEC.extensions || []) {
    if (!liveVoc[e.vocabulary]) { report.skipped.push(`terms for ${e.vocabulary}: vocabulary missing on instance`); continue; }
    for (const t of e.terms) {
      if (liveVoc[e.vocabulary].has(t.code)) { report.existing.push(`term ${e.vocabulary}.${t.code}`); continue; }
      plan.terms.push(T("as.dto.vocabulary.create.VocabularyTermCreation", { vocabularyId: VID(e.vocabulary), code: t.code, label: t.label, description: t.description }));
    }
  }
  const willPT = new Set(Object.keys(livePT));
  const willST = new Set(Object.keys(liveST));
  SPEC.object_types.forEach((o) => willST.add(o.code));
  const usable = (p, owner) => {
    if (livePT[p.code]) {
      if (livePT[p.code] !== dt(p.data_type)) { report.conflicts.push(`${owner}.${p.code}: instance has ${livePT[p.code]}, spec wants ${p.data_type}`); return false; }
      return true;
    }
    if (willPT.has(p.code)) return true;
    if (p.code.startsWith("$")) { report.skipped.push(`${owner}.${p.code}: internal property missing on instance`); return false; }
    if (p.vocabulary_code && !willVoc.has(p.vocabulary_code)) { report.skipped.push(`${owner}.${p.code}: vocabulary ${p.vocabulary_code} missing on instance (standard masterdata not synced)`); return false; }
    if (p.object_code && !willST.has(p.object_code)) { report.skipped.push(`${owner}.${p.code}: object type ${p.object_code} missing on instance`); return false; }
    plan.propertyTypes.push(T("as.dto.property.create.PropertyTypeCreation", {
      code: p.code, label: p.label, description: p.description || p.label, dataType: dt(p.data_type),
      ...(p.vocabulary_code ? { vocabularyId: VID(p.vocabulary_code) } : {}),
      ...(p.object_code ? { sampleTypeId: STID(p.object_code) } : {}),
    }));
    willPT.add(p.code);
    return true;
  };
  for (const o of SPEC.object_types) {
    const pas = [];
    // display order: optional section_order (e.g. workflow sections first), stable within a section
    const rank = (s) => { const i = (o.section_order || []).indexOf(s); return i < 0 ? 999 : i; };
    const props = o.properties.map((p, i) => [p, i]).sort((a, b) => rank(a[0].section) - rank(b[0].section) || a[1] - b[1]).map((x) => x[0]);
    props.forEach((p) => {
      if (!usable(p, o.code)) return;
      if (liveST[o.code] && liveST[o.code].has(p.code)) return;
      pas.push(T("as.dto.property.create.PropertyAssignmentCreation", {
        propertyTypeId: PTID(p.code), section: p.section, ordinal: pas.length + 1, mandatory: p.mandatory, showInEditView: true,
      }));
    });
    if (liveST[o.code]) {
      report.existing.push("object type " + o.code);
      if (pas.length) plan.assignments.push(T("as.dto.sample.update.SampleTypeUpdate", {
        typeId: STID(o.code), propertyAssignments: T("as.dto.common.update.ListUpdateValue", { actions: [T("as.dto.common.update.ListUpdateActionAdd", { items: pas })] }),
      }));
    } else {
      plan.sampleTypes.push(T("as.dto.sample.create.SampleTypeCreation", {
        code: o.code, description: o.description, generatedCodePrefix: o.generated_code_prefix, autoGeneratedCode: false, propertyAssignments: pas,
      }));
    }
  }

  const summary = {
    createVocabularies: plan.vocabularies.map((v) => v.code),
    addTerms: plan.terms.map((t) => t.vocabularyId.permId + "." + t.code),
    createPropertyTypes: plan.propertyTypes.map((p) => p.code),
    createObjectTypes: plan.sampleTypes.map((s) => `${s.code} (${s.propertyAssignments.length} props)`),
    addAssignments: plan.assignments.map((u) => u.typeId.permId),
    ...report,
  };
  if (dryRun) return { dryRun: true, ...summary };

  // ---- execute (dependency order) ------------------------------------------------------
  if (plan.vocabularies.length) await call("createVocabularies", plan.vocabularies);
  if (plan.terms.length) await call("createVocabularyTerms", plan.terms);
  if (plan.propertyTypes.length) await call("createPropertyTypes", plan.propertyTypes);
  if (plan.sampleTypes.length) await call("createSampleTypes", plan.sampleTypes);
  if (plan.assignments.length) await call("updateSampleTypes", plan.assignments);
  return { dryRun: false, ...summary };
}
