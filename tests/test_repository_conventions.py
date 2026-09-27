"""Guardrails for repository structure and imported-source provenance."""

import re
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "AGENTS.md",
    "ARCHITECTURE.md",
    "CATEGORIES.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "TO-DO.md",
    "imports/CATALOG.md",
    "imports/README.md",
    "pyproject.toml",
    "skills/README.md",
)

RUNTIME_IGNORE_PATTERNS = {
    ".skillctl/",
    "agent-memory/",
    "cache/",
    "credentials/",
    "indexes/",
    "installations/",
    "logs/",
    "sessions/",
}


def test_bootstrap_artifacts_are_present() -> None:
    """The repository retains the documented, reproducible foundation."""
    missing = [path for path in REQUIRED_FILES if not (REPOSITORY_ROOT / path).is_file()]
    assert not missing, f"Missing bootstrap artifacts: {', '.join(missing)}"


def test_runtime_state_is_ignored() -> None:
    """Canonical source stays separate from local runtime state."""
    ignore_patterns = set((REPOSITORY_ROOT / ".gitignore").read_text().splitlines())
    missing = sorted(RUNTIME_IGNORE_PATTERNS - ignore_patterns)
    assert not missing, f"Runtime paths must be ignored: {', '.join(missing)}"


def test_import_catalog_has_editorial_inventory_columns() -> None:
    """Imported sources require a human-readable rationale and audit trail."""
    catalog = (REPOSITORY_ROOT / "imports/CATALOG.md").read_text()
    expected_columns = (
        "| Importación | Estado | URL upstream | Commit fijado | Licencia |",
        "Capacidades aprovechadas | Racional | Límites de uso |",
    )
    missing = [column for column in expected_columns if column not in catalog]
    assert not missing, f"Missing catalog columns: {', '.join(missing)}"


def _catalog_rows(catalog: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in catalog.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells[0] == "Importación":
            continue
        assert len(cells) == 8, f"Catalog row must have eight columns: {line}"
        import_id = cells[0].strip("`")
        assert import_id not in rows, f"Duplicate catalog import: {import_id}"
        assert cells[1] in {"propuesto", "activo", "retirado"}
        assert cells[6], f"Catalog rationale is required for {import_id}"
        assert cells[7], f"Catalog limits are required for {import_id}"
        rows[import_id] = cells
    return rows


def _front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text().splitlines()
    assert lines and lines[0] == "---", f"Missing front matter in {path}"
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"Unclosed front matter in {path}") from error

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        assert separator and key and value.strip(), f"Invalid front matter in {path}: {line}"
        fields[key] = value.strip()
    return fields


def _submodule_urls() -> dict[str, str]:
    gitmodules = REPOSITORY_ROOT / ".gitmodules"
    if not gitmodules.exists():
        return {}

    result = subprocess.run(
        [
            "git",
            "config",
            "--file",
            str(gitmodules),
            "--get-regexp",
            r"^submodule\..*\.(path|url)$",
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    records: dict[str, dict[str, str]] = {}
    for line in result.stdout.splitlines():
        key, value = line.split(maxsplit=1)
        name, field = key.removeprefix("submodule.").rsplit(".", 1)
        records.setdefault(name, {})[field] = value
    return {record["path"]: record["url"] for record in records.values()}


def _gitlink_commit(path: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "ls-files", "--stage", "--", path],
        capture_output=True,
        check=True,
        text=True,
    )
    fields = result.stdout.strip().split()
    assert len(fields) >= 3, f"Missing gitlink for {path}"
    assert fields[0] == "160000", f"Import must be a gitlink: {path}"
    return fields[1]


def test_active_imports_have_consistent_provenance() -> None:
    """An active import is pinned and auditable across all three records."""
    catalog_rows = _catalog_rows((REPOSITORY_ROOT / "imports/CATALOG.md").read_text())
    active_ids = {import_id for import_id, row in catalog_rows.items() if row[1] == "activo"}
    sidecars = list((REPOSITORY_ROOT / "imports").glob("*/*.provenance.md"))
    sidecar_ids = set()
    submodule_urls = _submodule_urls()

    for sidecar in sidecars:
        fields = _front_matter(sidecar)
        required = {
            "import_id",
            "upstream_url",
            "commit",
            "upstream_ref",
            "license",
            "reviewed_by",
            "reviewed_on",
        }
        missing = required - fields.keys()
        assert not missing, f"Missing provenance fields in {sidecar}: {', '.join(sorted(missing))}"
        import_id = fields["import_id"]
        sidecar_ids.add(import_id)

        row = catalog_rows.get(import_id)
        assert row is not None, f"Missing catalog entry for {import_id}"
        assert row[1] in {"activo", "retirado"}, f"Sidecar has invalid status for {import_id}"
        assert row[2] == fields["upstream_url"]
        assert row[3] == fields["commit"]
        assert row[4] == fields["license"]

        if row[1] == "activo":
            path = f"imports/{import_id}"
            assert submodule_urls.get(path) == fields["upstream_url"]
            assert re.fullmatch(r"[0-9a-f]{40}", fields["commit"])
            assert _gitlink_commit(path) == fields["commit"]

    assert active_ids == sidecar_ids & active_ids, "Every active import needs a provenance sidecar"
