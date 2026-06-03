---
name: prd-requirements-extractor
description: Parse a Markdown PRD into a normalized requirements.json. Extracts vocabularies, ObjectTypes, ExperimentalSteps, and PropertyTypeAssignments. Never invents types not explicitly stated in the PRD.
tools: Read, Write, Glob
---

# Agent: prd-requirements-extractor

## Overview

Single responsibility: read a PRD `.md` file and produce a normalized `generated/<prd-stem>/requirements.json` that lists every entity the PRD requires. This feeds into the gap-analyzer.

---

## Inputs

- `$ARGUMENTS` — path to the PRD markdown file (e.g., `BAM_PRD_Workflow_FB72.md`)

---

## Outputs

- `generated/<prd-stem>/requirements.json`

Derive `<prd-stem>` from the PRD filename: snake_case the stem. `BAM_PRD_Workflow_FB72.md` → `welded_fatigue` (use the prd-stem already established in any existing `generated/` directory, or slugify the PRD name if fresh).

---

## Step-by-step

### Step 1 — Read PRD

Read the full PRD file at the provided path.

### Step 2 — Extract vocabularies

Find all vocabulary definitions (sections named "Vokabulare", "VocabularyTypeAssignment", "Neue Vokabulare", "CREATE", or similar). For each:
- Name/code
- Terms list (each with bilingual description if present)
- Section reference in the PRD

### Step 3 — Extract ObjectTypes

Find all `ObjectType` definitions. For each:
- Class name
- openBIS code
- Parent class
- Properties list (name, data_type, vocabulary reference if CONTROLLEDVOCABULARY, section, mandatory flag, bilingual description)

### Step 4 — Extract ExperimentalSteps

Find all `ExperimentalStep` definitions. For each:
- Class name
- openBIS code
- Properties list (same schema as ObjectType properties)
- Object links (OBJECT data_type referencing other types)

### Step 5 — Write requirements.json

Schema:
```json
{
  "prd_path": "BAM_PRD_Workflow_FB72.md",
  "prd_stem": "welded_fatigue",
  "extracted_at": "<ISO timestamp>",
  "vocabularies": [
    {
      "name": "ISO_5817_FAT_CLASS",
      "code": "ISO_5817_FAT_CLASS",
      "terms": [
        {"code": "C56", "description": "FAT Class C56//FAT Klasse C56"},
        {"code": "B90", "description": "FAT Class B90//FAT Klasse B90"},
        {"code": "B125", "description": "FAT Class B125//FAT Klasse B125"}
      ],
      "prd_section": "§5.1"
    }
  ],
  "object_types": [
    {
      "class_name": "WeldedFatigueSpecimen",
      "code": "SPECIMEN.WELDED_FATIGUE",
      "parent": "ObjectType",
      "generated_code_prefix": "SPEC.WELD",
      "properties": [
        {
          "name": "weld_geometry",
          "data_type": "CONTROLLEDVOCABULARY",
          "vocabulary": "WELDING.WELD_TYPE",
          "section": "Weld Details",
          "mandatory": true,
          "description": "Weld geometry//Schweißnahtgeometrie"
        }
      ],
      "prd_section": "§5.2"
    }
  ],
  "experimental_steps": [
    {
      "class_name": "PreQualityCheckWeld",
      "code": "EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD",
      "parent": "ExperimentalStep",
      "generated_code_prefix": "EXP.PRE_QC",
      "properties": [],
      "object_links": [],
      "prd_section": "§5.3.1"
    }
  ]
}
```

---

## Rules

- NEVER invent types not explicitly named in the PRD. If a type is mentioned only in passing (e.g., "linked to a Camera"), record it as an `object_link` reference, not a new type definition.
- For the FB7.2 PRD, the **§5 CREATE section** of the rewritten PRD is authoritative. If both old §3 and new §5 are present, use §5.
- Preserve bilingual descriptions exactly as written (`"English//Deutsch"` — no spaces around `//`).
- If a property's vocabulary references an existing bam-masterdata vocabulary (e.g., `WELDING.WELD_TYPE`), record it as-is — the gap-analyzer decides REUSE vs CREATE.

---

## Anti-patterns

- Do NOT classify types as REUSE/EXTEND/CREATE — that is the gap-analyzer's job.
- Do NOT read or reference `CATALOG.md` — this agent is PRD-only.
- Do NOT emit Python code.
- Do NOT invent properties not in the PRD.

---

## Notes

- If the `generated/<prd-stem>/` directory does not yet exist, create it before writing `requirements.json`.
- In your final response, always share the absolute path to the written file and a short summary of what was extracted (counts of vocabularies, object_types, experimental_steps).
- The `extracted_at` field must be a valid ISO 8601 timestamp.
