"""Tests use temporary real files; no synthetic rows enter GOV IA."""
import hashlib
from govia_agent_source.source_reader import inspect_repository


def test_source_bytes_and_sha256_are_real(tmp_path):
    content = b"from langgraph.graph import StateGraph\n"
    (tmp_path / "agent.py").write_bytes(content)
    result = inspect_repository(str(tmp_path))
    assert len(result) == 1
    assert result[0]["path"] == "agent.py"
    assert result[0]["sha256"] == hashlib.sha256(content).hexdigest()
    assert "langgraph" in result[0]["terms"]


def test_excluded_and_large_sources_are_not_read(tmp_path):
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "agent.py").write_text("ignored")
    (tmp_path / "large.py").write_bytes(b"a" * 64001)
    assert inspect_repository(str(tmp_path)) == []


def test_empty_repository_has_no_fabricated_evidence(tmp_path):
    assert inspect_repository(str(tmp_path)) == []
