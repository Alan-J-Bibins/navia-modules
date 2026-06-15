from activities.social_story.model import SocialStorySchema
from activities.social_story.utils import extract_story_text
from activities.social_story.evaluation.deterministic_analysis import (
    deterministic_analysis,
)
from activities.social_story.evaluation.readability_analysis import readability_analysis
from activities.social_story.evaluation.probabilistic_analysis import (
    probabilistic_analysis,
)


def evaluate_social_story(story: str | SocialStorySchema, target_age: int = 8) -> str:
    """
    Aggregates Deterministic, Algorithmic (Readability), and Probabilistic analyses
    into a unified report precisely calibrated for readers across their lifespan (Ages 3+).

    Args:
        story: The social story text or schema.
        target_age: Target age for algorithmic metrics (used if story is a raw string).
    """
    # 1. Normalize inputs for Analysis Tiers
    story_text = (
        extract_story_text(story) if isinstance(story, SocialStorySchema) else story
    )
    
    # Floor the system at 3 years old with no upper boundary ceiling
    raw_age = story.target_age if isinstance(story, SocialStorySchema) else target_age
    age = max(3, raw_age)
    scaling_age = min(18, age)

    # 2. Execute Analysis Tiers
    det_report = deterministic_analysis(story)
    rating_display = (
        "∞ (0 Coaching)"
        if det_report.story_rating == float("inf")
        else f"{det_report.story_rating:.2f}"
    )

    readability_report = readability_analysis(story_text, target_age=age)
    prob_report = probabilistic_analysis(story)

    # 3. Derive Failure Reasons (Purely from report data)
    tier1_reasons = []
    if det_report.second_person_pronouns:
        tier1_reasons.append("Contains second-person pronouns (you/your)")
    if det_report.absolute_constraints:
        tier1_reasons.append("Uses absolute constraints (must/should/never)")
    if not det_report.sentence_ratio_criteria:
        tier1_reasons.append(
            "Sentence ratio failed (Coaching sentences > 1 or Ratio < 4)"
        )

    # Dynamic target calculations matching readability_analysis matrix for accurate logs
    if scaling_age <= 5:
        max_grade = 0.5
        min_first = 95.0
        max_len = 6
        max_passives = 0
        max_pronouns = 0.20
        max_neg = 1.0
    elif scaling_age <= 9:
        max_grade = float(scaling_age - 5.0)
        min_first = 95.0 - (2.5 * (scaling_age - 7))
        max_len = 12
        max_passives = 0
        max_pronouns = 0.35
        max_neg = 1.5
    elif scaling_age <= 14:
        max_grade = float(scaling_age - 4.0)
        min_first = 80.0
        max_len = 15
        max_passives = 1
        max_pronouns = 0.50
        max_neg = 2.0
    else:
        max_grade = 10.0
        min_first = 70.0
        max_len = 18
        max_passives = 2
        max_pronouns = 0.60
        max_neg = 2.5

    tier2_reasons = []
    if readability_report.flesch_kincaid_grade > max_grade:
        tier2_reasons.append(
            f"Grade level too high ({readability_report.flesch_kincaid_grade} > {max_grade:.1f})"
        )
    if readability_report.first_readability_index < min_first:
        tier2_reasons.append(
            f"FIRST Readability Index too low ({readability_report.first_readability_index} < {min_first:.1f})"
        )
    if readability_report.max_sentence_length > max_len:
        tier2_reasons.append(
            f"Max sentence length exceeded ({readability_report.max_sentence_length} > {max_len})"
        )
    if readability_report.negation_density > max_neg:
        tier2_reasons.append(
            f"Negation density too high ({readability_report.negation_density}% > {max_neg}%)"
        )
    if readability_report.passive_voice_count > max_passives:
        tier2_reasons.append(
            f"Too many passive structures ({readability_report.passive_voice_count} > {max_passives})"
        )
    if readability_report.pronoun_noun_ratio > max_pronouns:
        tier2_reasons.append(
            f"Pronoun-to-Noun ratio too high ({readability_report.pronoun_noun_ratio} > {max_pronouns})"
        )

    # 4. Format Aggregated Report
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
