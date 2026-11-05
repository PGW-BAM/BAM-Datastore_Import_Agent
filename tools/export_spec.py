"""Export the desired openBIS state ("spec") from generated bam-masterdata classes.

Loads every module in a generated datamodel folder with the *real* bam-masterdata package
(so the code is import-tested on the way), and writes one JSON with:

  vocabularies   CREATE vocabularies (code, description, terms)
  extensions     EXTEND term additions (from extend.json next to the datamodel, optional)
  object_types   CREATE object types with ALL properties incl. inherited ones, in display order

German names: label_de (property_label_de / VocabularyTerm.label_de). bam-masterdata writes them to openBIS
as "English//Deutsch" (label + label_de), like the descriptions.

The JSON is the input for the idempotent apply step (tools/openbis_apply.js, run in the
signed-in browser session) or for `bam_masterdata` sync on an admin machine.

Usage (needs an interpreter with bam-masterdata installed):
  python tools/export_spec.py generated/welded_fatigue_v2/datamodel > generated/welded_fatigue_v2/spec.json
"""

from __future__ import annotations

import importlib.util
import inspect
import json
import sys
from pathlib import Path

from bam_masterdata.metadata.entities import ObjectType, VocabularyType


def load(path: Path):
    spec = importlib.util.spec_from_file_location(f"gen_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def prop(p) -> dict:
    d = p.model_dump(exclude_none=True)
    return {
        "code": d["code"],
        "data_type": str(getattr(p.data_type, "value", p.data_type)),
        "label": d.get("property_label", d["code"]),
        "label_de": d.get("property_label_de"),
        "description": d.get("description", ""),
        "section": d.get("section", ""),
        "mandatory": bool(d.get("mandatory", False)),
        "vocabulary_code": d.get("vocabulary_code"),
        "object_code": d.get("object_code"),
    }


def main(folder: str) -> None:
    folder = Path(folder)
    vocabs, objs = [], []
    for path in sorted(folder.glob("*.py")):
        if path.name.startswith("_"):
            continue
        mod = load(path)
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if cls.__module__ != mod.__name__:
                continue  # imported base classes are not ours
            if issubclass(cls, VocabularyType):
                v = cls()
                vocabs.append({
                    "code": cls.defs.code,
                    "description": cls.defs.description,
                    "terms": [{"code": t.code, "label": t.label, "label_de": t.label_de, "description": t.description}
                              for t in v.terms],
                })
            elif issubclass(cls, ObjectType):
                o = cls()
                objs.append({
                    "class": cls.__name__,
                    "parent": cls.__mro__[1].__name__,
                    "code": cls.defs.code,
                    "description": cls.defs.description,
                    "generated_code_prefix": cls.defs.generated_code_prefix,
                    "properties": [prop(p) for p in o.properties],
                })
    ext_file = folder / "extend.json"
    extensions = json.loads(ext_file.read_text(encoding="utf-8")) if ext_file.exists() else []
    out = {"vocabularies": vocabs, "extensions": extensions, "object_types": objs}
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
