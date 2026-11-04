<!-- Titel: Masterdata request: <Thema> (<Fachbereich>) -->
<!-- Ziel: https://github.com/BAMresearch/bam-masterdata/issues · Label-Vorschlag: semver:minor (neue Typen) -->

## Summary

<Fachbereich> documents <workflow> in the BAM Data Store. To do so we need **<n> new object types**, **<n> new
vocabularies** and **<n> additions** to existing definitions. Everything else reuses bam-masterdata as is
(checked against release v0.17.0, `datamodel/v0`).

Contribution: Python modules (attached, ready for a PR) **and** `masterdata.xlsx` (attached). Contact: <Name>, Data Store Steward <Fachbereich>.

## Why

<2–4 sentences: what the lab needs to trace, which questions the data must answer later.>

## New (CREATE)

| Code | Kind | Parent (v0) | Why no existing type fits |
|---|---|---|---|
| | object type | | closest peer: `<code>` (`<file>:<line>`) lacks … |
| | vocabulary | | |

## Additions to existing definitions (EXTEND)

| Existing definition | Citation | Addition | Why |
|---|---|---|---|
| | `bam_masterdata/datamodel/v0/<file>.py:<line>` | term `<CODE>` "<English//Deutsch>" | |

## Instance sync only (no PR needed)

Defined in bam-masterdata but missing or outdated on `<instance>` (export of <date>):

| Definition | Status on instance |
|---|---|
| | missing / fewer properties |

## Expected impact

- Existing data / parsers: <none, only additions>
- Compatibility: no renamed or removed properties, nothing made mandatory

## Checks

- `bam_masterdata checker --mode individual`: <0 errors, n warnings> (log attached; explained below)
- import test with bam-masterdata v0.17.0: passed

<warnings explained, e.g. inherited `$ANNOTATIONS_STATE` deprecation comes from `SAMPLE` itself>

## Ontology mapping notes (optional)

| New code | Closest BFO/IAO/PMD concept | Note |
|---|---|---|
