"""Real LangGraph agent: inspect a Git checkout and create evidence-linked notes.

The application creates NO governance decisions. A model can explain source
observations but cannot assert identity, compliance, or certification authority.
"""
import json
import os
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from .source_reader import inspect_repository


class AnalysisState(TypedDict):
    repository_path: str
    question: str
    evidence: list[dict]
    answer: str


def collect_source_evidence(state: AnalysisState) -> dict:
    return {"evidence": inspect_repository(state["repository_path"])}


def explain_evidence(state: AnalysisState) -> dict:
    files = state["evidence"]
    if not files:
        return {"answer": "No supported source files were found; no claims can be made."}
    if not os.getenv("OPENAI_API_KEY"):
        citations = ", ".join(item["path"] for item in files[:12])
        return {"answer": f"Inspected {len(files)} real files. Sources: {citations}. "
                          "AI interpretation not run (OPENAI_API_KEY absent). "
                          "Governance state: NOT_EVIDENCED."}

    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model=os.getenv("GOVIA_MODEL", "gpt-4.1-mini"), temperature=0)
    observations = [{"path": f["path"], "sha256": f["sha256"], "terms": f["terms"]} for f in files]
    instruction = (
        "You are a source-intelligence assistant, not a governance authority. "
        "Only report source observations explicitly supported by the supplied file citations. "
        "Mention path and sha256 for each observation. Never invent code content, "
        "canonical identity, risk rating, compliance, or certification. "
        "If evidence is insufficient, say NOT_EVIDENCED."
    )
    user = f"Question: {state['question']}\nActual repository evidence:\n{json.dumps(observations, ensure_ascii=False)}"
    response = model.invoke([("system", instruction), ("human", user)])
    return {"answer": str(response.content)}


def create_agent():
    """A real, executable LangGraph workflow with two processing nodes."""
    graph = StateGraph(AnalysisState)
    graph.add_node("collect_evidence", collect_source_evidence)
    graph.add_node("explain_evidence", explain_evidence)
    graph.add_edge(START, "collect_evidence")
    graph.add_edge("collect_evidence", "explain_evidence")
    graph.add_edge("explain_evidence", END)
    return graph.compile()


class RepositoryAnalysisAgent:
    """Runnable LangGraph agent that produces evidence-backed source observations.

    Its structural declaration enables discovery, not governance approval.
    """
    kind = "agent"

    def __init__(self) -> None:
        self.workflow = create_agent()

    def run(self, repository_path: str, question: str) -> AnalysisState:
        return self.workflow.invoke({
            "repository_path": repository_path,
            "question": question,
            "evidence": [],
            "answer": "",
        })


def analyze(repository_path: str, question: str) -> AnalysisState:
    return RepositoryAnalysisAgent().run(repository_path, question)
