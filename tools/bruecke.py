"""openBIS-Brücke als ein Befehl, für das BAM-Netz. Gleiche Logik wie notebooks/openbis_bruecke.ipynb.

  python tools/bruecke.py <projekt> lesen         Export der Instanz            (Schritt 3, 7)
  python tools/bruecke.py <projekt> pruefen       lesen + Soll/Ist-Prüfung      (Schritt 7)
  python tools/bruecke.py <projekt> trockenlauf   lesen + prüfen + Plan zeigen  (Schritt 8, vor ◆ E)
  python tools/bruecke.py <projekt> anlegen       lesen + prüfen + anlegen      (Schritt 8, nach ◆ E)

Der Befehl holt vorher den neuesten Stand (git pull) und schiebt hinterher nur die Ergebnisdateien des
Projekts zurück (git commit + push). Mit --ohne-git passiert beides nicht. Arbeitet der Agent auf einem eigenen
Zweig, nennt AUFGABE.md ihn: --zweig <name> wechselt vorher dorthin.

Anmeldung: Umgebungsvariable OPENBIS_TOKEN (Personal Access Token), sonst fragt der Befehl nach Token oder
Benutzername/Passwort. Nichts davon wird gespeichert.

anlegen: verweigert, solange die Prüfung Lücken meldet (--trotz-luecken nur für Tests auf dem Playground),
zeigt den Trockenlauf und fragt vor dem Schreiben nach „ja“ (--ja überspringt die Frage).
"""

from __future__ import annotations

import argparse
import getpass
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openbis_bridge as ob  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
ACTIONS = ("lesen", "pruefen", "trockenlauf", "anlegen")


def git(repo: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def git_switch(repo: Path, branch: str) -> None:
    if git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == branch:
        return
    git(repo, "fetch", "origin", branch)
    r = git(repo, "checkout", branch)
    if r.returncode:
        sys.exit(f"Wechsel auf Zweig {branch} ging nicht:\n" + (r.stderr or r.stdout) +
                 "\nLokale Änderungen? Erst committen oder verwerfen.")
    print("Zweig:", branch)


def git_pull(repo: Path) -> None:
    r = git(repo, "pull", "--ff-only")
    if r.returncode:
        sys.exit("git pull ging nicht:\n" + (r.stderr or r.stdout) +
                 "\nLokale Änderungen? Erst committen oder verwerfen, oder mit --ohne-git arbeiten.")
    print("git pull:", (r.stdout.strip().splitlines() or ["ok"])[-1])


def git_push(repo: Path, pdir: Path, message: str) -> None:
    rel = pdir.relative_to(repo).as_posix()
    git(repo, "add", "--", rel)
    if git(repo, "diff", "--cached", "--quiet", "--", rel).returncode == 0:
        print("git: keine neuen Dateien zum Hochladen")
        return
    r = git(repo, "commit", "-m", message, "--", rel)
    if r.returncode:
        sys.exit("git commit ging nicht:\n" + (r.stderr or r.stdout))
    r = git(repo, "push")
    if r.returncode:
        sys.exit("git push ging nicht (der Commit ist lokal gespeichert, später `git push`):\n" + (r.stderr or r.stdout))
    print(f"git: hochgeladen ({message})")


def login(instance: str):
    token = os.environ.get("OPENBIS_TOKEN", "").strip()
    if not token:
        token = getpass.getpass(f"openBIS-Token für {instance} (leer = Benutzername/Passwort): ").strip()
    if token:
        return ob.connect(instance, token)
    from pybis import Openbis

    o = Openbis(instance)
    o.login(input("Benutzername: "), getpass.getpass("Passwort: "), save_token=False)
    return o, ob.v3_caller(o)


def run(project: dict, action: str, call, yes: bool = False, despite_gaps: bool = False, ask=input) -> int:
    """The work itself (no git, no login), so it can be tested with a fake openBIS."""
    today = date.today().isoformat()
    inv = ob.read_inventory(call, project["instance"], project["read_projects"])
    ob.write_json(project["inventory"], inv)
    print(f"gelesen: {len(inv['objectTypes'])} Object-Types, {len(inv['objects'])} Objekte in "
          f"{len(project['read_projects'])} Projekten -> {project['inventory'].name}")
    if action == "lesen":
        return 0

    spec, structure = ob.read_json(project["spec"]), ob.read_json(project["structure"])
    rep = ob.check(inv, spec, structure)
    md = ob.render_check_md(rep)
    (project["dir"] / "delivery_check.md").write_text(md + "\n", encoding="utf-8")
    ob.save_report(project["dir"], "check", rep)
    print(md)
    if action == "pruefen":
        return 0 if rep["ready"] else 2

    if structure is None:
        print(f"Keine structure.json ({project['structure']}). Die schreibt der Agent in Schritt 8.")
        return 1
    plan = ob.apply(call, structure, project["structure"].parent, dry_run=True)
    ob.save_report(project["dir"], "dryrun", plan)
    print(f"\nTrockenlauf: würde anlegen {len(plan['created'])}, schon da {len(plan['skipped'])}, "
          f"nicht zugewiesene Properties {len(plan['droppedProps'])}")
    for i in plan["created"]:
        print("  +", i)
    for i in plan["droppedProps"]:
        print("  ! nicht zugewiesen:", i)
    if action == "trockenlauf":
        print(f"\nPrüfseite E erzeugt der Agent daraus: python tools/render_review.py {project['name']} trockenlauf")
        return 0

    if not rep["ready"] and not despite_gaps:
        print("\nNicht angelegt: Die Prüfung meldet Lücken (siehe oben). Erst beheben.")
        return 2
    if not plan["created"]:
        print("\nNichts anzulegen.")
        return 0
    if not yes and ask(f"\n{len(plan['created'])} Einträge auf {project['instance']} anlegen? (ja/nein) ").strip().lower() != "ja":
        print("Abgebrochen, nichts angelegt.")
        return 1
    done = ob.apply(call, structure, project["structure"].parent, dry_run=False)
    done["instance"] = project["instance"]
    ob.write_json(project["dir"] / "reports" / f"apply_{today}.json", done)
    print(f"angelegt: {len(done['created'])}, übersprungen: {len(done['skipped'])}")
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows consoles: never crash on a character they cannot show
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="openBIS-Brücke (BAM-Netz): lesen, prüfen, Trockenlauf, anlegen")
    ap.add_argument("projekt", help="Ordner unter projects/")
    ap.add_argument("aktion", choices=ACTIONS)
    ap.add_argument("--ja", action="store_true", help="beim Anlegen nicht nachfragen")
    ap.add_argument("--trotz-luecken", action="store_true", help="anlegen, obwohl die Prüfung Lücken meldet (nur Tests)")
    ap.add_argument("--zweig", help="vorher auf diesen git-Zweig wechseln (steht in AUFGABE.md)")
    ap.add_argument("--ohne-git", action="store_true", help="kein git pull vorher, kein commit/push hinterher")
    ap.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    if not a.ohne_git:
        if a.zweig:
            git_switch(a.repo, a.zweig)
        git_pull(a.repo)
    project = ob.load_project(a.repo, a.projekt)
    print(f"Projekt {a.projekt}: {project['instance']}  {project['read_projects'][0]}")
    o, call = login(project["instance"])
    try:
        code = run(project, a.aktion, call, yes=a.ja, despite_gaps=a.trotz_luecken)
    finally:
        try:
            o.logout()
        except Exception:  # noqa: BLE001
            pass
    if not a.ohne_git:
        git_push(a.repo, project["dir"], f"{a.projekt}: {a.aktion} {date.today().isoformat()}")
    return code


if __name__ == "__main__":
    sys.exit(main())
