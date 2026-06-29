from pydantic import BaseModel, Field

from activities.social_story.model import SocialStorySchema
from activities.social_story.utils import extract_story_text
from activities.social_story.evaluation.deterministic_analysis import (
    deterministic_analysis,
    DeterministicAnalysisReport,
)
from activities.social_story.evaluation.readability_analysis import (
    readability_analysis,
    ReadabilityAnalysisReport,
)
from activities.social_story.evaluation.probabilistic_analysis import (
    probabilistic_analysis,
    ProbabilisticAnalysisReport,
    QualitativeMatrix,
)


# ── JSON Response Models ────────────────────────────────────────────────


class Tier1Result(BaseModel):
    second_person_pronouns: bool
    absolute_constraints: bool
    sentence_ratio_criteria: bool
    story_rating: float
    tier1_passed: bool
    failure_reasons: list[str]


class Tier2Result(BaseModel):
    flesch_kincaid_grade: float
    first_readability_index: float
    max_sentence_length: int
    negation_density: float
    passive_voice_count: int
    pronoun_noun_ratio: float
    passed_all_guardrails: bool
    failure_reasons: list[str]


class Tier3Result(BaseModel):
    qualitative_reviews: QualitativeMatrix | None = None
    constructive_feedback: list[str] = []
    tier3_passed: bool | None = None
    error: str | None = None


class EvaluationReportResponse(BaseModel):
    tier1: Tier1Result | None = None
    tier2: Tier2Result | None = None
    tier3: Tier3Result | None = None
    overall_passed: bool = Field(
        description="True if all *evaluated* tiers passed. Disabled tiers are excluded."
    )


# ── Shared Helpers ──────────────────────────────────────────────────────


def _get_age_thresholds(scaling_age: int) -> dict:
    """Returns age-calibrated thresholds for Tier 2 readability guardrails."""
    if scaling_age <= 5:
        return dict(
            max_grade=0.5, min_first=95.0, max_len=6,
            max_passives=0, max_pronouns=0.20, max_neg=1.0,
        )
    elif scaling_age <= 9:
        return dict(
            max_grade=float(scaling_age - 5.0),
            min_first=95.0 - (2.5 * (scaling_age - 7)),
            max_len=12, max_passives=0, max_pronouns=0.35, max_neg=1.5,
        )
    elif scaling_age <= 14:
        return dict(
            max_grade=float(scaling_age - 4.0),
            min_first=80.0, max_len=15,
            max_passives=1, max_pronouns=0.50, max_neg=2.0,
        )
    else:
        return dict(
            max_grade=10.0, min_first=70.0, max_len=18,
            max_passives=2, max_pronouns=0.60, max_neg=2.5,
        )


def _compute_tier1_reasons(det_report: DeterministicAnalysisReport) -> list[str]:
    reasons = []
    if det_report.second_person_pronouns:
        reasons.append("Contains second-person pronouns (you/your)")
    if det_report.absolute_constraints:
        reasons.append("Uses absolute constraints (must/should/never)")
    if not det_report.sentence_ratio_criteria:
        reasons.append(
            "Sentence ratio failed (Coaching sentences > 1 or Ratio < 4)"
        )
    return reasons


def _compute_tier2_reasons(
    report: ReadabilityAnalysisReport, thresholds: dict
) -> list[str]:
    reasons = []
    if report.flesch_kincaid_grade > thresholds["max_grade"]:
        reasons.append(
            f"Grade level too high ({report.flesch_kincaid_grade} > {thresholds['max_grade']:.1f})"
        )
    if report.first_readability_index < thresholds["min_first"]:
        reasons.append(
            f"FIRST Readability Index too low ({report.first_readability_index} > {thresholds['min_first']:.1f})"
        )
    if report.max_sentence_length > thresholds["max_len"]:
        reasons.append(
            f"Max sentence length exceeded ({report.max_sentence_length} > {thresholds['max_len']})"
        )
    if report.negation_density > thresholds["max_neg"]:
        reasons.append(
            f"Negation density too high ({report.negation_density}% > {thresholds['max_neg']}%)"
        )
    if report.passive_voice_count > thresholds["max_passives"]:
        reasons.append(
            f"Too many passive structures ({report.passive_voice_count} > {thresholds['max_passives']})"
        )
    if report.pronoun_noun_ratio > thresholds["max_pronouns"]:
        reasons.append(
            f"Pronoun-to-Noun ratio too high ({report.pronoun_noun_ratio} > {thresholds['max_pronouns']})"
        )
    return reasons


# ── Existing string report (unchanged behavior, all tiers always run) ──


def evaluate_social_story(story: str | SocialStorySchema, target_age: int = 8) -> str:
    """
    Aggregates Deterministic, Algorithmic (Readability), and Probabilistic analyses
    into a unified report precisely calibrated for readers across their lifespan (Ages 3+).

    Args:
        story: The social story text or schema.
        target_age: Target age for algorithmic metrics (used if story is a raw string).
    """
    story_text = (
        extract_story_text(story) if isinstance(story, SocialStorySchema) else story
    )
    raw_age = story.target_age if isinstance(story, SocialStorySchema) else target_age
    age = max(3, raw_age)
    scaling_age = min(18, age)

    det_report = deterministic_analysis(story)
    rating_display = (
        "∞ (0 Coaching)"
        if det_report.story_rating == float("inf")
        else f"{det_report.story_rating:.2f}"
    )

    readability_report = readability_analysis(story_text, target_age=age)
    prob_report = probabilistic_analysis(story)

    thresholds = _get_age_thresholds(scaling_age)
    tier1_reasons = _compute_tier1_reasons(det_report)
    tier2_reasons = _compute_tier2_reasons(readability_report, thresholds)

    lines = [
        "=" * 50,
        "SOCIAL STORY EVALUATION REPORT",
        "=" * 50,
        "",
        "--- TIER 1: DETERMINISTIC CHECKS ---",
        f"  Second Person Pronouns: {'FAIL' if det_report.second_person_pronouns else 'PASS'}",
        f"  Absolute Constraints:   {'FAIL' if det_report.absolute_constraints else 'PASS'}",
        f"  Sentence Ratio:         {'PASS' if det_report.sentence_ratio_criteria else 'FAIL'}",
        f"  Story Rating:           {rating_display}",
        f"  TIER 1 STATUS:          {'PASSED' if det_report.tier1_passed else 'FAILED'}",
    ]
    if tier1_reasons:
        lines.append("  REASONS:")
        for r in tier1_reasons:
            lines.append(f"     • {r}")

    lines.extend(
        [
            "",
            "--- TIER 2: ALGORITHMIC METRICS ---",
            f"  Flesch-Kincaid Grade:   {readability_report.flesch_kincaid_grade}",
            f"  FIRST Index:            {readability_report.first_readability_index}",
            f"  Negation Density:       {readability_report.negation_density}%",
            f"  Passive Voice Count:    {readability_report.passive_voice_count}",
            f"  Pronoun-to-Noun Ratio:  {readability_report.pronoun_noun_ratio}",
            f"  Max Sentence Length:    {readability_report.max_sentence_length}",
            f"  TIER 2 STATUS:          {'PASSED' if readability_report.passed_all_guardrails else 'FAILED'}",
        ]
    )
    if tier2_reasons:
        lines.append("  REASONS:")
        for r in tier2_reasons:
            lines.append(f"     • {r}")

    if prob_report:
        q = prob_report.qualitative_reviews
        lines.extend(
            [
                "",
                "--- TIER 3: QUALITATIVE REVIEW ---",
                f"  Goal Alignment:       {q.goal_alignment}/5",
                f"  Structural Cohesion:  {q.structural_cohesion}/5",
                f"  Literal Precision:    {q.literal_precision}/5",
                f"  Social Rationale:     {q.social_rationale}/5",
                f"  TIER 3 STATUS:         {'PASSED' if prob_report.tier3_passed else 'FAILED'}",
                "",
                "--- CONSTRUCTIVE FEEDBACK ---",
            ]
        )
        for fb in prob_report.constructive_feedback:
            lines.append(f"  • {fb}")
    else:
        lines.extend(
            [
                "",
                "--- TIER 3: QUALITATIVE REVIEW ---",
                "  ERROR: Failed to generate qualitative report.",
            ]
        )
    lines.append("=" * 50)
    return "\n".join(lines)


# ── JSON helper with tier toggles ───────────────────────────────────────


def evaluate_social_story_as_dict(
    story: str | SocialStorySchema,
    target_age: int = 8,
    tier1_enabled: bool = True,
    tier2_enabled: bool = True,
    tier3_enabled: bool = True,
) -> dict:
    """
    Runs the evaluation tiers that are enabled and returns a JSON-serializable dict.

    Disabled tiers are omitted from the response (set to null) and their
    analysis is never executed — saving LLM calls for tier3 and computation
    for tiers 1/2.

    Args:
        story: The social story text or schema.
        target_age: Target age for algorithmic metrics.
        tier1_enabled: Run deterministic checks.
        tier2_enabled: Run readability analysis.
        tier3_enabled: Run probabilistic/qualitative review.
    """
    # 1. Normalize inputs
    story_text = (
        extract_story_text(story) if isinstance(story, SocialStorySchema) else story
    )
    raw_age = story.target_age if isinstance(story, SocialStorySchema) else target_age
    age = max(3, raw_age)
    scaling_age = min(18, age)

    # 2. Conditionally execute tiers
    det_report = deterministic_analysis(story) if tier1_enabled else None
    readability_report = readability_analysis(story_text, target_age=age) if tier2_enabled else None
    prob_report = probabilistic_analysis(story) if tier3_enabled else None

    thresholds = _get_age_thresholds(scaling_age)

    # 3. Build tier1 result
    if det_report:
        tier1_reasons = _compute_tier1_reasons(det_report)
        safe_rating = det_report.story_rating
        if safe_rating == float("inf"):
            safe_rating = -1.0
        tier1_result = Tier1Result(
            second_person_pronouns=det_report.second_person_pronouns,
            absolute_constraints=det_report.absolute_constraints,
            sentence_ratio_criteria=det_report.sentence_ratio_criteria,
            story_rating=safe_rating,
            tier1_passed=det_report.tier1_passed,
            failure_reasons=tier1_reasons,
        )
    else:
        tier1_result = None

    # 4. Build tier2 result
    if readability_report:
        tier2_reasons = _compute_tier2_reasons(readability_report, thresholds)
        tier2_result = Tier2Result(
            flesch_kincaid_grade=readability_report.flesch_kincaid_grade,
            first_readability_index=readability_report.first_readability_index,
            max_sentence_length=readability_report.max_sentence_length,
            negation_density=readability_report.negation_density,
            passive_voice_count=readability_report.passive_voice_count,
            pronoun_noun_ratio=readability_report.pronoun_noun_ratio,
            passed_all_guardrails=readability_report.passed_all_guardrails,
            failure_reasons=tier2_reasons,
        )
    else:
        tier2_result = None

    # 5. Build tier3 result
    if prob_report:
        tier3_result = Tier3Result(
            qualitative_reviews=prob_report.qualitative_reviews,
            constructive_feedback=prob_report.constructive_feedback,
            tier3_passed=prob_report.tier3_passed,
        )
    elif tier3_enabled:
        # Tier was enabled but LLM call failed
        tier3_result = Tier3Result(error="Failed to generate qualitative report.")
    else:
        tier3_result = None

    # 6. Compute overall_passed from *evaluated* tiers only
    tier_results = []
    if tier1_result:
        tier_results.append(tier1_result.tier1_passed)
    if tier2_result:
        tier_results.append(tier2_result.passed_all_guardrails)
    if tier3_result and tier3_result.tier3_passed is not None:
        tier_results.append(tier3_result.tier3_passed)

    overall_passed = all(tier_results) if tier_results else True

    # 7. Assemble response
    report = EvaluationReportResponse(
        tier1=tier1_result,
        tier2=tier2_result,
        tier3=tier3_result,
        overall_passed=overall_passed,
    )

    return report.model_dump()
