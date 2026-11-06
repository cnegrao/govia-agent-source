import pytest

pytest.importorskip("langgraph")

from govia_agent_source.agent import create_agent


def test_workflow_uses_actual_repository_file(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    (tmp_path / "agent.py").write_text("from langgraph.graph import StateGraph\n")
    workflow = create_agent()
    result = workflow.invoke({"repository_path": str(tmp_path), "question": "Which frameworks?", "evidence": [], "answer": ""})
    assert len(result["evidence"]) == 1
    assert result["evidence"][0]["path"] == "agent.py"
    assert "NOT_EVIDENCED" in result["answer"]
