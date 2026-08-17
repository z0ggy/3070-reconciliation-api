from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TypedDict, cast

BASE_DIR: Path = Path(__file__).resolve().parent
PROJECT_ROOT: Path = BASE_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.geo_types import MatchCandidate
from src.match import match_data
from src.type_detection import EntityType

"""
Save the accuracy metrics of the matcher results, for a manual created evaluation
data sprint5_eval_data.json

References:
    - https://github.com/lirt1231/MPLR/blob/main/eval/evaluate.py
    - https://pythonexamples.org/python-unpack-dictionary/
    - https://spotintelligence.com/2024/08/02/mean-reciprocal-rank-mrr/
    - https://stackoverflow.com/questions/40412714/using-json-dumps-with-ensure-ascii-true
"""

EVALUATION_FILE: Path = BASE_DIR / "sprint5_eval_data.json"
RESULTS_FILE: Path = BASE_DIR / "sprint5_evaluation_results.json"
METRICS_FILE: Path = BASE_DIR / "sprint5_evaluation_metrics.json"
EVALUATION_LIMIT = 100  # extend default(10) limit for matcher to retain all candidates above threshold.


class EvaluationCase(TypedDict):
    """Represent a row loaded from the evaluation dataset."""

    case_id: str
    category: str
    query: str
    expected_id: str | None
    expected_type: EntityType | None
    expected_match: bool


class EvaluationResult(EvaluationCase):
    """Represents results dict."""

    expected_rank: int | None
    top1_success: bool | None
    top3_success: bool | None
    no_match_success: bool | None
    returned_candidates: list[MatchCandidate]


class Metrics(TypedDict):
    """Represents metrics dict."""

    total_cases: int
    positive_cases: int
    no_match_cases: int
    top1_correct: int
    top1_accuracy: float
    top3_correct: int
    top3_accuracy: float
    mrr: float
    correct_no_match: int
    no_match_accuracy: float
    false_positive_count: int
    false_positive_rate: float


def load_cases(path: Path) -> list[EvaluationCase]:
    """Load evaluation dataset from file."""

    with path.open("r", encoding="utf-8") as file:
        return cast(list[EvaluationCase], json.load(file))


def find_expected_candidate_rank(
    candidates: list[MatchCandidate],
    expected_id: str | None,
) -> int | None:
    """Return the rank of the expected candidate id or None."""

    for position, candidate in enumerate(candidates, start=1):
        if candidate["id"] == expected_id:
            return position

    return None


def evaluate() -> tuple[Metrics, list[EvaluationResult]]:
    """
    The evaluation case runner where:
    top1_correct: expected candidates ranked first/all match_count
    top3_correct: expected candidates in range (1-3) (when top1 fails)
    rr_rank_sum: used to compute MRR (Mean Reciprocal Rank)
    """

    # Store all cases
    evaluation_cases: list[EvaluationCase] = load_cases(EVALUATION_FILE)

    # All cases where "expected_match: true" from evaluation_cases
    match_count = 0

    # All cases where "expected_match: false" from evaluation_cases
    no_match_count = 0

    top1_correct = 0
    top3_correct = 0
    rr_rank_sum: float = 0.0

    # When the matcher correctly returned zero candidates.
    correct_no_match = 0

    results: list[EvaluationResult] = []

    for case in evaluation_cases:
        # Run and store all evaluation cases through the matcher.
        candidates: list[MatchCandidate] = match_data(
            query=case["query"],
            limit=EVALUATION_LIMIT,
        )

        # Where "expected_match: true" from cases
        if case["expected_match"]:
            match_count += 1

            expected_rank: int | None = find_expected_candidate_rank(
                candidates,
                expected_id=case["expected_id"],
            )

            # Logic for distinguish top1 and top3
            top1_success: bool = expected_rank == 1
            top3_success: bool = expected_rank is not None and expected_rank <= 3

            if top1_success:
                top1_correct += 1

            if top3_success:
                top3_correct += 1

            if expected_rank is not None:
                # Calculate/update reciprocal rank
                rr_rank_sum += 1 / expected_rank

            results.append(
                {
                    **case,  # unpacks the case dict EvaluationCase and build a new dict
                    "expected_rank": expected_rank,
                    "top1_success": top1_success,
                    "top3_success": top3_success,
                    "no_match_success": None,
                    "returned_candidates": candidates,
                }
            )

        else:  # Where "expected_match: false" from cases
            no_match_count += 1

            no_match_success: bool = len(candidates) == 0

            if no_match_success:
                correct_no_match += 1

            results.append(
                {
                    **case,
                    "expected_rank": None,
                    "top1_success": None,
                    "top3_success": None,
                    "no_match_success": no_match_success,
                    "returned_candidates": candidates,
                }
            )

    # A case where the matcher still returned a candidate.
    false_positive_count: int = no_match_count - correct_no_match

    # Aggregate results in metrics
    metrics: Metrics = {
        "total_cases": len(evaluation_cases),
        "positive_cases": match_count,
        "no_match_cases": no_match_count,
        "top1_correct": top1_correct,
        "top1_accuracy": (top1_correct / match_count if match_count else 0.0),
        "top3_correct": top3_correct,
        "top3_accuracy": (top3_correct / match_count if match_count else 0.0),
        "mrr": (rr_rank_sum / match_count if match_count else 0.0),
        "correct_no_match": correct_no_match,
        "no_match_accuracy": (
            correct_no_match / no_match_count if no_match_count else 0.0
        ),
        "false_positive_count": false_positive_count,
        "false_positive_rate": (
            false_positive_count / no_match_count if no_match_count else 0.0
        ),
    }

    return metrics, results


def save_json(path: Path, data: Metrics | list[EvaluationResult]) -> None:
    """Write metrics/results."""

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )


def print_metrics(metrics: Metrics) -> None:
    """Print summary of the evaluation metrics."""

    print("Sprint 5 Evaluation")
    print("-------------------")
    print(f"Total cases: {metrics['total_cases']}")
    print(f"Positive cases: {metrics['positive_cases']}")
    print(f"No-match cases: {metrics['no_match_cases']}")
    print()

    top1_ratio: str = f"{metrics['top1_correct']}/{metrics['positive_cases']}"
    print(f"Top-1 accuracy: {top1_ratio} ({metrics['top1_accuracy']:.2%})")

    top3_ratio: str = f"{metrics['top3_correct']}/{metrics['positive_cases']}"
    print(f"Top-3 accuracy: {top3_ratio} ({metrics['top3_accuracy']:.2%})")

    print(f"MRR: {metrics['mrr']:.3f}")

    no_match_ratio: str = f"{metrics['correct_no_match']}/{metrics['no_match_cases']}"
    print(f"No-match accuracy: {no_match_ratio} ({metrics['no_match_accuracy']:.2%})")

    fp_ratio: str = f"{metrics['false_positive_count']}/{metrics['no_match_cases']}"
    print(f"False-positive rate: {fp_ratio} ({metrics['false_positive_rate']:.2%})")


if __name__ == "__main__":
    metrics, results = evaluate()

    # Save summary metrics with details.
    save_json(METRICS_FILE, metrics)
    save_json(RESULTS_FILE, results)

    print_metrics(metrics)

    print()
    print(f"Metrics saved to: {METRICS_FILE}")
    print(f"Detailed results saved to: {RESULTS_FILE}")
