#!/usr/bin/env python3
"""Validate evidence-driven product architecture HTML reports.

Structural validation is backward compatible. Add ``--quality visual`` for
new deliverables that must satisfy the skill's responsive, accessible, and
print-ready presentation baseline.
"""

from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


PROFILES = {
    "generic": [],
    "journey": ["scope", "evidence", "journey", "issues"],
    "agents": ["scope", "agents", "contracts", "tools", "context", "dataflow"],
    "single-agent": ["scope", "input", "output", "tools", "state", "rules", "prompt", "trace", "tests", "unknowns"],
    "architecture": [
        "summary", "evidence", "domains", "e2e", "layers", "relations",
        "context", "knowledge", "models", "tech", "entities", "sequence",
        "panorama", "asis", "tobe", "risks", "trace", "unknowns",
    ],
    "comparison": [
        "scope", "thesis", "comparison", "architecture", "common",
        "incomparable", "selection", "fusion", "risks", "evidence",
        "unknowns",
    ],
}


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.h2: list[str] = []
        self._in_h2 = False
        self._h2_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(data["id"] or "")
        if data.get("href"):
            self.hrefs.append(data["href"] or "")
        if tag == "h2":
            self._in_h2 = True
            self._h2_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_h2:
            self._h2_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            title = "".join(self._h2_parts).strip()
            if title:
                self.h2.append(title)
            self._in_h2 = False


def validate(path: Path, profile: str, quality: str = "structure") -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"File not found: {path}"]

    text = path.read_text(encoding="utf-8")
    if len(text) < 2000:
        errors.append("Report is too small to be a complete HTML deliverable")
    if "<!doctype html" not in text.lower():
        errors.append("Missing <!doctype html>")
    if "<html" not in text.lower() or "</html>" not in text.lower():
        errors.append("Missing complete <html> document")

    parser = ReportParser()
    parser.feed(text)

    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate ids: {', '.join(duplicates)}")

    missing = [item for item in PROFILES[profile] if item not in parser.ids]
    if missing:
        errors.append(f"Missing required section ids for {profile}: {', '.join(missing)}")

    internal = [href for href in parser.hrefs if href.startswith("#") and href[1:] not in parser.ids]
    if internal:
        errors.append(f"Broken internal links: {', '.join(internal)}")

    broken_local: list[str] = []
    for href in parser.hrefs:
        if not href or href.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        target = (path.parent / href.split("#", 1)[0]).resolve()
        if not target.exists():
            broken_local.append(href)
    if broken_local:
        errors.append(f"Broken local links: {', '.join(broken_local)}")

    if profile == "architecture":
        if text.count('class="mermaid"') < 3:
            errors.append("Architecture report must contain at least 3 Mermaid blocks")
        for label in ("已确认", "合理推断", "建议设计", "未知"):
            if label not in text:
                errors.append(f"Missing evidence label: {label}")
    elif profile == "single-agent":
        for marker in ("System Prompt", "stateDiagram-v2", "测试"):
            if marker not in text:
                errors.append(f"Missing single-agent marker: {marker}")

    if profile == "comparison":
        for label in ("已确认", "合理推断", "建议设计", "未知"):
            if label not in text:
                errors.append(f"Missing evidence label: {label}")

    if quality == "visual":
        lower = text.lower()
        checks = {
            "Missing html language declaration": re.search(r"<html[^>]+\blang=", lower),
            "Missing viewport meta": re.search(r"<meta[^>]+name=[\"']viewport[\"']", lower),
            "Missing meta description": re.search(r"<meta[^>]+name=[\"']description[\"']", lower),
            "Missing semantic navigation": "<nav" in lower,
            "Missing semantic main region": "<main" in lower,
            "Missing color-scheme support": "color-scheme" in lower,
            "Missing system dark-mode styles": "prefers-color-scheme" in lower,
            "Missing responsive media query": re.search(r"@media\s*\([^)]*(max-width|min-width)", lower),
            "Missing print styles": re.search(r"@media\s+print", lower),
            "Missing keyboard focus-visible style": ":focus-visible" in lower,
            "Missing reduced-motion handling": "prefers-reduced-motion" in lower,
            "Missing anchor scroll offset": "scroll-margin" in lower,
        }
        for message, passed in checks.items():
            if not passed:
                errors.append(message)

        if "<table" in lower and not re.search(
            r"overflow(?:-x)?\s*:\s*(?:auto|scroll)", lower
        ):
            errors.append("Tables exist but no horizontal overflow container is defined")

        body_rule = re.search(r"body\s*\{([^}]+)\}", lower)
        body_has_16px = bool(
            body_rule
            and (
                re.search(r"font-size\s*:\s*(?:1rem|1[6-9](?:\.0+)?px)", body_rule.group(1))
                or re.search(r"font\s*:[^;}]*\b(?:1rem|1[6-9](?:\.0+)?px)/", body_rule.group(1))
            )
        )
        if not body_has_16px:
            errors.append("Body reading text does not declare a 16px baseline")

    if not parser.h2:
        errors.append("No <h2> section headings found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--profile", choices=sorted(PROFILES), default="generic")
    parser.add_argument(
        "--quality",
        choices=("structure", "visual"),
        default="structure",
        help="Use visual for responsive, accessible, and print-ready deliverables",
    )
    args = parser.parse_args()

    errors = validate(args.html.resolve(), args.profile, args.quality)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: {args.html.resolve()} ({args.profile}, {args.quality})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
