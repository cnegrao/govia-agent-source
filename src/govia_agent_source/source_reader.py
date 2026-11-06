"""Read real repository files without executing repository code."""
from dataclasses import asdict, dataclass
from pathlib import Path

ALLOWED = {".py", ".ts", ".tsx", ".js", ".json", ".toml", ".yaml", ".yml", ".md"}
EXCLUDED = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}
MAX_FILES = 100
MAX_FILE_BYTES = 64_000


@dataclass(frozen=True)
class SourceEvidence:
    path: str
    sha256: str
    bytes_read: int
    terms: tuple[str, ...]

    def as_dict(self) -> dict:
        return asdict(self)


def inspect_repository(directory: str, max_files: int = MAX_FILES) -> list[dict]:
    """Return citations to actual file bytes. No fabricated source records."""
    import hashlib

    root = Path(directory).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Repository path must be an existing directory")
    results: list[dict] = []
    for path in sorted(root.rglob("*")):
        if len(results) >= max_files:
            break
        if not path.is_file() or path.suffix.lower() not in ALLOWED:
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED for part in relative.parts):
            continue
        if path.is_symlink() or path.stat().st_size > MAX_FILE_BYTES:
            continue
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        needles = ("langgraph", "langchain", "openai", "anthropic", "crewai", "mcp", "agent", "tool")
        terms = tuple(term for term in needles if term in text.lower())
        results.append(SourceEvidence(
            path=relative.as_posix(),
            sha256=hashlib.sha256(data).hexdigest(),
            bytes_read=len(data),
            terms=terms,
        ).as_dict())
    return results
