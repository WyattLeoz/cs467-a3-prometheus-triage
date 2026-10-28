#!/usr/bin/env python3
"""Check triage decision/output consistency before publication and during evaluation.

This module has no GitHub access and never rewrites proposals. The trusted publishing
job reads the agent's final session message and proposed outputs; missing evidence or
an invalid combination fails closed. Semantic correctness remains an evaluation task.
"""
import argparse
import json
import re
from pathlib import Path


def outputs_match(decision, labels, comments):
    """Return whether published/proposed labels and comments fit the declared decision."""
    if (len(labels) > 2 or len(comments) > 1
            or any(not isinstance(label, str) for label in labels)
            or any(not isinstance(comment, str) or not comment.strip() for comment in comments)
            or len(set(labels)) != len(labels)):
        return False
    components = sum(label.startswith("component/") for label in labels)
    if components > 1:
        return False
    if decision == "NO_ACTION":
        return not labels and not comments
    if decision in {"OTHER_PROJECT", "SECURITY"}:
        return not labels and len(comments) == 1
    if decision == "POSSIBLE_DUPLICATE":
        return len(comments) == 1 and all(label.startswith("component/") for label in labels)
    if decision == "NEEDS_INFO":
        return len(comments) == 1 and set(labels) <= {"kind/more-info-needed"}
    if decision == "SUPPORT_QUESTION":
        return len(comments) == 1 and set(labels) <= {"kind/question"}
    if decision == "ROUTE":
        return bool(labels) and not comments and all(
            label.startswith("component/") or label in {"kind/feature", "kind/enhancement"}
            for label in labels)
    return False


def final_decision(events):
    """Read the final assistant message from Copilot events; ignore tool/user content."""
    messages = [event["data"].get("content", "") for event in events
                if isinstance(event, dict) and isinstance(event.get("data"), dict)
                and event.get("type") == "assistant.message"
                and not event.get("data", {}).get("toolRequests")]
    if not messages or not isinstance(messages[-1], str):
        raise ValueError("missing final assistant message")
    match = re.match(r"\ADecision: ([A-Z_]+)\b", messages[-1])
    if not match:
        raise ValueError("final message must start with Decision: <DECISION>")
    return match.group(1)


def validate_proposal(proposal, decision):
    """Reject malformed or inconsistent safe-output proposals without modifying them."""
    if not isinstance(proposal, dict):
        raise ValueError("proposal must be an object")
    items = proposal.get("items")
    if not isinstance(items, list) or proposal.get("errors"):
        raise ValueError("missing output items or safe-output errors")
    labels, comments, calls = [], [], []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("output item must be an object")
        kind = item.get("type")
        if kind not in {"add_labels", "add_comment", "noop"} or kind in calls:
            raise ValueError("unknown or repeated triage output call")
        calls.append(kind)
        if kind == "add_labels":
            values = item.get("labels")
            if not isinstance(values, list) or not values:
                raise ValueError("labels must be a nonempty list")
            labels = [value.get("name") if isinstance(value, dict) else value for value in values]
        elif kind == "add_comment":
            comments.append(item.get("body"))
    if not outputs_match(decision, labels, comments):
        raise ValueError(f"proposed outputs do not match decision {decision}")
    if decision == "NO_ACTION" and calls != ["noop"]:
        raise ValueError("NO_ACTION requires exactly one noop")


def main():
    """Validate the downloaded proposal/session artifacts; exit nonzero to block publishing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    args = parser.parse_args()
    try:
        sessions = list(args.artifact_root.glob("**/copilot-session-state/*/events.jsonl"))
        if len(sessions) != 1:
            raise ValueError(f"expected one agent session, found {len(sessions)}")
        events = [json.loads(line) for line in sessions[0].read_text(encoding="utf-8").splitlines() if line.strip()]
        decision = final_decision(events)
        proposal = json.loads((args.artifact_root / "agent_output.json").read_text(encoding="utf-8"))
        validate_proposal(proposal, decision)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f"Triage publication blocked: {error}\n")
    print(f"Triage output policy passed: {decision}")


if __name__ == "__main__":
    main()
