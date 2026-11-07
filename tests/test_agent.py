import pytest

pytest.importorskip("langgraph")

from govia_agent_source.agent import RepositoryAnalysisAgent, analyze, create_agent


def test_workflow_uses_actual_repository_file(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    (tmp_path / "agent.py").write_text("from langgraph.graph import StateGraph\n")
    workflow = create_agent()
    result = workflow.invoke({"repository_path": str(tmp_path), "question": "Which frameworks?", "evidence": [], "answer": ""})
    assert len(result["evidence"]) == 1
    assert result["evidence"][0]["path"] == "agent.py"
    assert "NOT_EVIDENCED" in result["answer"]


def test_declared_agent_executes_real_langgraph_workflow(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    (tmp_path / "sample.py").write_text("from langgraph.graph import StateGraph\n")

    instance = RepositoryAnalysisAgent()
    assert instance.kind == "agent"
    result = instance.run(str(tmp_path), "Which frameworks?")
    assert [item["path"] for item in result["evidence"]] == ["sample.py"]
    assert "NOT_EVIDENCED" in result["answer"]

    public_result = analyze(str(tmp_path), "Which frameworks?")
    assert public_result["evidence"] == result["evidence"]


def test_agent_declares_scanner_recognized_kind():
    import inspect
    import re

    declaration = inspect.getsource(RepositoryAnalysisAgent)
    assert re.search(r"(?m)^\s*kind\s*=\s*[\"']agent[\"']\s*$", declaration)
