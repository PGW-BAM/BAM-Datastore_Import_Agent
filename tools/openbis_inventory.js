// Read-only inventory of an openBIS 20.10 instance (V3 JSON-RPC), run inside a signed-in ELN tab.
// "Inventory in" handover for cloud sessions (CLOUD.md): only search* calls, nothing is created or changed.
// No credentials involved: the session token is taken from the browser cookie of the user's own login.
//
//   const inv = await inventory();
//   copy(JSON.stringify(inv, null, 1));   // DevTools: to clipboard
//   -> save as generated/live/<instance>_inventory.json and commit; the agent writes <instance>_inventory.md

async function inventory() {
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
  // V3 JSON sends repeated objects once and later only their numeric @id
  const search = async (method, criteria, fetchOptions) => {
    const res = await call(method, T(criteria), fetchOptions);
    const ids = {}; (function w(o) { if (o && typeof o === "object") { if (o["@id"] !== undefined) ids[o["@id"]] = o; for (const k in o) w(o[k]); } })(res);
    return { objects: res.objects, ref: (o) => (typeof o === "number" ? ids[o] : o) };
  };
  const ident = (x) => (x && typeof x === "object" ? x.identifier || x.permId : x);
  const PA = T("as.dto.property.fetchoptions.PropertyAssignmentFetchOptions", { propertyType: T("as.dto.property.fetchoptions.PropertyTypeFetchOptions") });
  const typesWithProps = async (method, criteria, fetchOptions) => {
    const { objects, ref } = await search(method, criteria, T(fetchOptions, { propertyAssignments: PA }));
    return objects.map((t) => ({
      code: t.code, description: t.description || null,
      ...(t.generatedCodePrefix !== undefined ? { generatedCodePrefix: t.generatedCodePrefix } : {}),
      properties: (t.propertyAssignments || []).map(ref).sort((a, b) => a.ordinal - b.ordinal).map((a) => {
        const p = ref(a.propertyType);
        return { code: p.code, dataType: p.dataType, section: a.section || null, mandatory: !!a.mandatory };
      }),
    }));
  };

  const vocs = await search("searchVocabularies", "as.dto.vocabulary.search.VocabularySearchCriteria",
    T("as.dto.vocabulary.fetchoptions.VocabularyFetchOptions", { terms: T("as.dto.vocabulary.fetchoptions.VocabularyTermFetchOptions") }));
  const pts = await search("searchPropertyTypes", "as.dto.property.search.PropertyTypeSearchCriteria",
    T("as.dto.property.fetchoptions.PropertyTypeFetchOptions", { vocabulary: T("as.dto.vocabulary.fetchoptions.VocabularyFetchOptions"), sampleType: T("as.dto.sample.fetchoptions.SampleTypeFetchOptions") }));
  const projects = await search("searchProjects", "as.dto.project.search.ProjectSearchCriteria", T("as.dto.project.fetchoptions.ProjectFetchOptions"));
  const exps = await search("searchExperiments", "as.dto.experiment.search.ExperimentSearchCriteria",
    T("as.dto.experiment.fetchoptions.ExperimentFetchOptions", { type: T("as.dto.experiment.fetchoptions.ExperimentTypeFetchOptions") }));

  const inv = {
    instance: location.origin,
    collected: new Date().toISOString(),
    server: await call("getServerInformation").catch(() => null),
    vocabularies: vocs.objects.map((v) => ({ code: v.code, description: v.description || null, terms: (v.terms || []).map(vocs.ref).map((t) => t.code) })),
    propertyTypes: pts.objects.map((p) => ({
      code: p.code, label: p.label, dataType: p.dataType,
      vocabulary: p.vocabulary ? pts.ref(p.vocabulary).code : null, objectType: p.sampleType ? pts.ref(p.sampleType).code : null,
    })),
    objectTypes: await typesWithProps("searchSampleTypes", "as.dto.sample.search.SampleTypeSearchCriteria", T("as.dto.sample.fetchoptions.SampleTypeFetchOptions")),
    collectionTypes: await typesWithProps("searchExperimentTypes", "as.dto.experiment.search.ExperimentTypeSearchCriteria", T("as.dto.experiment.fetchoptions.ExperimentTypeFetchOptions")),
    datasetTypes: await typesWithProps("searchDataSetTypes", "as.dto.dataset.search.DataSetTypeSearchCriteria", T("as.dto.dataset.fetchoptions.DataSetTypeFetchOptions")),
    projects: projects.objects.map((p) => ident(p.identifier)),
    collections: exps.objects.map((e) => ({ identifier: ident(e.identifier), type: exps.ref(e.type).code })),
  };
  console.log(`inventory: ${inv.objectTypes.length} object types, ${inv.collectionTypes.length} collection types, ` +
    `${inv.datasetTypes.length} dataset types, ${inv.vocabularies.length} vocabularies, ${inv.collections.length} collections`);
  return inv;
}
