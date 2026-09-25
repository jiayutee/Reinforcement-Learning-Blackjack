"""Render a control export as a GitHub-readable, evidence-labelled policy table."""

import argparse
import json
import math
from pathlib import Path
import re

RULES = "foundations-v1: replacement draws, S17, no natural bonus, hit/stand"


def index_states(report):
    if not isinstance(report, dict) or report.get("schema_version") != 1 or report.get("artifact_type") != "monte_carlo_control" or report.get("rules") != RULES or report.get("gamma") != 1:
        raise ValueError("Expected a Foundations Monte Carlo control export, not a V(s) export.")
    training = report.get("training", {})
    if not isinstance(training, dict) or type(training.get("episodes")) is not int or training["episodes"] < 1 or type(training.get("environment_seed")) is not int:
        raise ValueError("Invalid training metadata.")
    epsilon = training.get("epsilon")
    if type(epsilon) not in (int, float) or not math.isfinite(epsilon) or not 0 <= epsilon <= 1:
        raise ValueError("Invalid epsilon.")
    if not isinstance(report.get("states"), list):
        raise ValueError("Expected the full states list, not a compact experiment record.")
    indexed = {}
    for row in report["states"]:
        if not isinstance(row, dict):
            raise ValueError("Invalid state row.")
        state = row.get("observation")
        if not isinstance(state, list) or len(state) != 3 or type(state[0]) is not int or not 4 <= state[0] <= 21 or type(state[1]) is not int or not 1 <= state[1] <= 10 or type(state[2]) is not bool:
            raise ValueError("Invalid observation.")
        key = tuple(state)
        if key in indexed:
            raise ValueError("Duplicate state.")
        actions = row.get("actions")
        if not isinstance(actions, list) or len(actions) != 2:
            raise ValueError("Both action entries are required.")
        by_action = {}
        for action in actions:
            if not isinstance(action, dict) or type(action.get("action")) is not int or action["action"] not in (0, 1) or action["action"] in by_action:
                raise ValueError("Invalid or duplicate action.")
            count, value = action.get("visits"), action.get("value")
            if type(count) is not int or not 0 <= count <= training["episodes"]:
                raise ValueError("Invalid action visit count.")
            if count == 0:
                if value is not None:
                    raise ValueError("An unvisited action must have a null estimate.")
            elif type(value) not in (int, float) or not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError("Invalid action value.")
            by_action[action["action"]] = action
        expected = int((by_action[1]["value"] or 0.0) > (by_action[0]["value"] or 0.0))
        if type(row.get("greedy_action")) is not int or row["greedy_action"] != expected:
            raise ValueError("Stored decision does not match Q values and the stand-on-ties rule.")
        indexed[key] = {"greedy_action": expected, "actions": by_action}
    return indexed


def cell(row, minimum_visits):
    if row is None:
        return "—"
    minimum = min(item["visits"] for item in row["actions"].values())
    if minimum == 0:
        return "?"
    return ("H" if row["greedy_action"] else "S") + ("*" if minimum < minimum_visits else "")


def render_policy_table(report, minimum_visits=20):
    if type(minimum_visits) is not int or minimum_visits < 1:
        raise ValueError("Minimum visits must be a positive integer.")
    rows = index_states(report)
    training = report["training"]
    lines = ["# Learned hit/stand table", "", "A snapshot of one trained policy, not an optimal blackjack strategy or a win-probability chart.", "",
             f"Training: {training['episodes']:,} hands, seed {training['environment_seed']}, epsilon {training['epsilon']}.",
             "Rules: replacement draws, dealer stands on soft 17, no natural bonus, hit/stand only.", "",
             "`H` = hit; `S` = stand. Decisions use the greater estimated Q; ties prefer stand.",
             f"`*` = at least one action has fewer than {minimum_visits} visits. This is a count warning, not a confidence interval.",
             "`?` = at least one action has never been tried; no evidence-backed comparison is shown. The actual evaluator still uses zero initialization for missing estimates.",
             "`—` = no observed decision at that position; some cells represent impossible hands. None of these marks means zero value.", ""]
    for soft in (False, True):
        lines += ["## " + ("Soft hands: a usable ace counts as 11" if soft else "Hard hands: no usable ace"), "",
                  "| Your total / dealer | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for total in range(21, 3, -1):
            marks = ["`" + cell(rows.get((total, dealer, soft)), minimum_visits) + "`" for dealer in range(1, 11)]
            lines.append("| " + str(total) + " | " + " | ".join(marks) + " |")
        lines.append("")
    lines += ["## Inspect the evidence", "", "| State (total, dealer, usable ace) | Stand Q / visits | Hit Q / visits | Display |", "|---|---|---|---|"]
    for state in ((12, 6, False), (16, 10, False), (18, 9, True), (20, 10, False)):
        row = rows.get(state)
        entries = []
        for action in (0, 1):
            item = row["actions"][action] if row else {"visits": 0, "value": None}
            entries.append("unknown / 0" if item["value"] is None else f"{item['value']:+.5f} / {item['visits']}")
        lines.append(f"| {state} | {entries[0]} | {entries[1]} | `{cell(row, minimum_visits)}` |")
    source = report.get("source")
    if isinstance(source, dict):
        revision = source.get("git_commit")
        if isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}", revision):
            dirty = source.get("foundations_source_dirty")
            status = str(dirty) if type(dirty) is bool else "unknown"
            lines += ["", f"Data source commit: `{revision}`. Foundations source dirty: `{status}`."]
    lines += ["", "The count cutoff changes only the warning marks, not the estimates or policy. Even unmarked decisions can be noisy or wrong. Compare multiple training seeds before generalizing.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-visits", type=int, default=20)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must be different files.")
    try:
        text = render_policy_table(json.loads(args.input.read_text()), args.minimum_visits)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    print(f"Saved policy table: {args.output.resolve()}")


if __name__ == "__main__":
    main()
