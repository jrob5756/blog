#!/usr/bin/env python3
"""
Sync news reports from the news repo into Hugo content.

Transforms reports/YYYY/MM/DD.md → content/news/YYYY-MM-DD.md
with Hugo front matter (title, date, summary from first paragraph).

Usage:
    python3 scripts/sync-news.py <reports_dir> <output_dir> [--today | --date YYYY-MM-DD | --since YYYY-MM-DD]

Examples:
    python3 scripts/sync-news.py /tmp/news/reports content/news/                  # all reports
    python3 scripts/sync-news.py /tmp/news/reports content/news/ --today           # today only
    python3 scripts/sync-news.py /tmp/news/reports content/news/ --date 2026-03-15 # specific date
    python3 scripts/sync-news.py /tmp/news/reports content/news/ --since 2026-03-01 # from date onward
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path


def extract_summary(content: str, max_length: int = 300) -> str:
    """Extract a summary from the first substantive paragraph of content."""
    lines = content.strip().split("\n")
    paragraph_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        # Skip headings and empty lines at the start
        if not paragraph_lines:
            if not stripped or stripped.startswith("#"):
                continue
        # Once we've started collecting, an empty line ends the paragraph
        if paragraph_lines and not stripped:
            break
        if not stripped.startswith("#"):
            paragraph_lines.append(stripped)

    summary = " ".join(paragraph_lines)
    # Strip markdown links, keeping the text
    summary = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", summary)
    # Strip bold/italic markers
    summary = re.sub(r"\*+", "", summary)

    if len(summary) > max_length:
        summary = summary[: max_length - 3].rsplit(" ", 1)[0] + "..."

    return summary


def format_date_title(year: str, month: str, day: str) -> str:
    """Format a human-readable title from date components."""
    d = date(int(year), int(month), int(day))
    return d.strftime("News Summary for %B %-d, %Y")


def extract_date_from_path(report_path: Path) -> tuple[str, str, str] | None:
    """Extract (year, month, day) from a report path like reports/YYYY/MM/DD.md."""
    parts = report_path.parts
    for i, part in enumerate(parts):
        if re.match(r"^\d{4}$", part) and i + 2 < len(parts):
            year = part
            month = parts[i + 1]
            day = parts[i + 2].replace(".md", "")
            return year, month, day
    return None


def report_date(report_path: Path) -> date | None:
    """Parse the date from a report's file path."""
    parts = extract_date_from_path(report_path)
    if parts is None:
        return None
    year, month, day = parts
    try:
        return date(int(year), int(month), int(day))
    except ValueError:
        return None


def process_report(report_path: Path, output_path: Path) -> bool:
    """
    Process a single news report file.

    Returns True if the file was written, False if skipped.
    """
    content = report_path.read_text(encoding="utf-8")

    # Skip if already has Hugo front matter
    if content.startswith("---"):
        return False

    parts = extract_date_from_path(report_path)
    if parts is None:
        print(f"  Skipping {report_path}: could not extract date from path")
        return False

    year, month, day = parts
    date_str = f"{year}-{month}-{day}"
    title = format_date_title(year, month, day)
    summary = extract_summary(content)

    # Build Hugo front matter
    front_matter = f"""---
title: "{title}"
date: {date_str}
summary: "{summary.replace('"', '\\"')}"
tags: ["news"]
categories: ["news"]
ShowReadingTime: true
---

"""

    output_file = output_path / f"{date_str}.md"
    output_file.write_text(front_matter + content, encoding="utf-8")
    return True


def collect_report_files(reports_path: Path) -> list[Path]:
    """Collect all valid report .md files, excluding _index.md and README."""
    files = []
    for f in sorted(reports_path.rglob("*.md")):
        if f.name.startswith("_") or f.name.lower() == "readme.md":
            continue
        files.append(f)
    return files


def sync_reports(
    reports_dir: str,
    output_dir: str,
    *,
    only_date: date | None = None,
    since_date: date | None = None,
) -> None:
    """Sync news reports from reports_dir to output_dir, with optional date filtering."""
    reports_path = Path(reports_dir)
    output_path = Path(output_dir)

    if not reports_path.exists():
        print(f"Error: Reports directory not found: {reports_dir}")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    report_files = collect_report_files(reports_path)

    # Apply date filters
    if only_date is not None:
        report_files = [f for f in report_files if report_date(f) == only_date]
    elif since_date is not None:
        report_files = [f for f in report_files if (d := report_date(f)) is not None and d >= since_date]

    if not report_files:
        filter_desc = ""
        if only_date:
            filter_desc = f" for {only_date.isoformat()}"
        elif since_date:
            filter_desc = f" since {since_date.isoformat()}"
        print(f"No reports found{filter_desc}")
        return

    written = 0
    skipped = 0

    for report_file in report_files:
        try:
            if process_report(report_file, output_path):
                written += 1
                print(f"  Synced: {report_file}")
            else:
                skipped += 1
        except Exception as e:
            print(f"  Error processing {report_file}: {e}")
            skipped += 1

    print(f"\nSync complete: {written} written, {skipped} skipped")


def parse_date(value: str) -> date:
    """Parse a YYYY-MM-DD date string."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {value} (expected YYYY-MM-DD)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync news reports from the news repo into Hugo content.",
    )
    parser.add_argument("reports_dir", help="Path to reports directory (e.g. /tmp/news/reports)")
    parser.add_argument("output_dir", help="Path to Hugo content output (e.g. content/news/)")

    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--today",
        action="store_true",
        help="Only sync today's report",
    )
    date_group.add_argument(
        "--date",
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Only sync a specific date's report",
    )
    date_group.add_argument(
        "--since",
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Sync reports from this date onward",
    )

    args = parser.parse_args()

    only_date = None
    since_date = None

    if args.today:
        only_date = date.today()
    elif args.date:
        only_date = args.date
    elif args.since:
        since_date = args.since

    filter_desc = "all reports"
    if only_date:
        filter_desc = only_date.isoformat()
    elif since_date:
        filter_desc = f"since {since_date.isoformat()}"

    print(f"Syncing {filter_desc} from {args.reports_dir} to {args.output_dir}...")
    sync_reports(args.reports_dir, args.output_dir, only_date=only_date, since_date=since_date)


if __name__ == "__main__":
    main()
