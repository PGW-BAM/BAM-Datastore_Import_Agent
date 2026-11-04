"""Request package (workflow step 6) and its review page, from the FB 7.2 example (offline, no bam_masterdata tools)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import build_request as br  # noqa: E402
import render_review as rr  # noqa: E402


def test_collect_counts_and_german_names():
    r = br.collect(ROOT, "fb72_welded_fatigue")
    assert len(r["new_types"]) == 2 and len(r["new_vocabularies"]) == 6 and len(r["new_properties"]) == 33
    assert sum(len(e["terms"]) for e in r["extensions"]) == 4
    assert all(p.get("label_de") for p in r["new_properties"])
    assert {x["code"] for x in r["reused_types"]} >= {"EXPERIMENTAL_STEP"}


def test_issue_and_mail_texts():
    r = br.collect(ROOT, "fb72_welded_fatigue")
    r["checker"] = {"ran": True, "errors": 0, "warnings": 1, "warning_texts": ["Property $ANNOTATIONS_STATE is deprecated"]}
    issue = br.issue_md(r)
    for part in ("## New object types", "## New property types", "## Additions to existing vocabularies",
                 "Herkunftsblech", "0 errors", "all inherited from the standard itself"):
        assert part in issue, part
    mail = br.mail_txt(r)
    assert mail.startswith("An: datastore@bam.de\nBetreff: Masterdaten-Antrag FB 7.2")
    assert "Mit freundlichen Grüßen" in mail and " du " not in mail and " dein" not in mail


def test_antrag_page_has_gate_lock_and_copy_blocks():
    m = rr.Model(ROOT, "fb72_welded_fatigue")
    html = rr.view_antrag(m)
    assert 'data-gate="C"' in html and 'class="send locked"' in html
    for cid in ("c-title", "c-issue", "c-subject", "c-mail", "out-d"):
        assert f'id="{cid}"' in html, cid
    assert "issues/new?title=" in html and m.missing == set()
