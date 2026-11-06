"""Command-line entry point for actual Git checkout scanning."""
import argparse
import json

from .agent import analyze


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real evidence-backed LangGraph analysis")
    parser.add_argument("repository", help="Path of a checked-out Git repository")
    parser.add_argument("--question", default="What AI agent technologies are declared?")
    args = parser.parse_args()
    result = analyze(args.repository, args.question)
    print(json.dumps({"answer": result["answer"], "evidence": result["evidence"]}, indent=2))


if __name__ == "__main__":
    main()
