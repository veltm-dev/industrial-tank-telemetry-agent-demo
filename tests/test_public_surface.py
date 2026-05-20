from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def test_internal_prep_files_are_not_tracked():
    forbidden = {
        "AGENTS.md",
        "docs/email-draft.md",
        "docs/video-script.md",
    }

    assert forbidden.isdisjoint(tracked_files())


def test_public_markdown_and_html_do_not_include_internal_prep_language():
    forbidden_phrases = [
        "".join(["Co", "dex", " Agent Instructions"]),
        " ".join(["Email", "Draft"]),
        " ".join(["Video", "Script"]),
        " ".join(["Hi", "[Name]"]),
        "[" + "phone" + "]",
        "[" + "email" + "]",
        "[" + "recording" + " " + "link" + "]",
        " ".join(["routed", "to", "you"]),
        " ".join(["after", "calling"]),
        " ".join(["one-day", "credibility", "packet"]),
        " ".join(["credibility", "packet"]),
        " ".join(["demo", "script"]),
    ]

    public_text_files = [
        path
        for path in tracked_files()
        if Path(path).suffix.lower() in {".md", ".html"}
    ]

    for path in public_text_files:
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in forbidden_phrases:
            assert phrase not in text, f"{phrase!r} found in {path}"
