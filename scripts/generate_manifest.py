from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT / "config" / "project.template.json"
ACTIVE_CONFIG_PATH = ROOT / "config" / "project.json"


@dataclass(slots=True)
class MaterialEntry:
    category: str
    relative_path: str
    filename: str
    stem: str
    suffix: str
    size_bytes: int
    modified_at: str


def resolve_path(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_config(config_arg: str | None) -> tuple[dict[str, Any], Path]:
    if config_arg:
        config_path = resolve_path(config_arg)
    elif ACTIVE_CONFIG_PATH.exists():
        config_path = ACTIVE_CONFIG_PATH
    else:
        config_path = DEFAULT_CONFIG_PATH

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    return load_json(config_path), config_path


def ensure_directories(paths: dict[str, str]) -> None:
    for value in paths.values():
        resolve_path(value).mkdir(parents=True, exist_ok=True)


def collect_entries(base_dir: Path, category: str, suffixes: list[str]) -> list[MaterialEntry]:
    normalized_suffixes = {suffix.lower() for suffix in suffixes}
    entries: list[MaterialEntry] = []

    if not base_dir.exists():
        return entries

    for file_path in sorted(base_dir.rglob("*")):
        if not file_path.is_file():
            continue
        if normalized_suffixes and file_path.suffix.lower() not in normalized_suffixes:
            continue

        stat = file_path.stat()
        entries.append(
            MaterialEntry(
                category=category,
                relative_path=file_path.relative_to(ROOT).as_posix(),
                filename=file_path.name,
                stem=file_path.stem,
                suffix=file_path.suffix.lower(),
                size_bytes=stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            )
        )

    return entries


def write_json_manifest(output_path: Path, entries: list[MaterialEntry], project_name: str) -> None:
    payload = {
        "project_name": project_name,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_items": len(entries),
        "items": [asdict(entry) for entry in entries],
    }
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def write_csv_manifest(output_path: Path, entries: list[MaterialEntry]) -> None:
    fieldnames = [
        "category",
        "relative_path",
        "filename",
        "stem",
        "suffix",
        "size_bytes",
        "modified_at",
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(asdict(entry))


def write_summary(output_path: Path, config_path: Path, counts: dict[str, int], total_items: int) -> None:
    lines = [
        f"generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"config_path: {config_path}",
        f"total_items: {total_items}",
    ]
    for category in ("raw", "audio", "subtitles"):
        lines.append(f"{category}: {counts.get(category, 0)}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan material folders and generate a manifest.")
    parser.add_argument(
        "--config",
        dest="config_path",
        default=None,
        help="Optional config path. Relative paths are resolved from the workspace root.",
    )
    args = parser.parse_args()

    config, config_path = load_config(args.config_path)
    paths = config["paths"]
    scan = config["scan"]
    project_name = config.get("project_name", "clip-automation")

    ensure_directories(paths)

    category_specs = [
        ("raw", resolve_path(paths["raw_materials"]), scan["raw_extensions"]),
        ("audio", resolve_path(paths["audio_materials"]), scan["audio_extensions"]),
        ("subtitles", resolve_path(paths["subtitle_materials"]), scan["subtitle_extensions"]),
    ]

    entries: list[MaterialEntry] = []
    counts: dict[str, int] = {}
    for category, base_dir, suffixes in category_specs:
        category_entries = collect_entries(base_dir, category, suffixes)
        counts[category] = len(category_entries)
        entries.extend(category_entries)

    jobs_dir = resolve_path(paths["jobs"])
    logs_dir = resolve_path(paths["logs"])
    jobs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    json_output = jobs_dir / "material_manifest.json"
    csv_output = jobs_dir / "material_manifest.csv"
    summary_output = logs_dir / "manifest_summary.txt"

    write_json_manifest(json_output, entries, project_name)
    write_csv_manifest(csv_output, entries)
    write_summary(summary_output, config_path, counts, len(entries))

    print(f"Config loaded: {config_path}")
    print(f"Manifest JSON: {json_output}")
    print(f"Manifest CSV: {csv_output}")
    print(f"Summary log: {summary_output}")
    print(f"Totals -> raw: {counts.get('raw', 0)}, audio: {counts.get('audio', 0)}, subtitles: {counts.get('subtitles', 0)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
