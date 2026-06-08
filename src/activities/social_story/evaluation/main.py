from activities.social_story.model import SocialStorySchema
from activities.social_story.utils import extract_story_text
from activities.social_story.evaluation.deterministic_analysis import (
    deterministic_analysis,
)
from activities.social_story.evaluation.algorithmic_analysis import algorithmic_analysis
from activities.social_story.evaluation.probabilistic_analysis import (
    probabilistic_analysis,
)


def evaluate_social_story(story: str | SocialStorySchema, target_age: int = 8) -> str:
    """
    Aggregates Deterministic, Algorithmic, and Probabilistic analyses into a unified report.

    Args:
        story: The social story text or schema.
        target_age: Target age for algorithmic metrics (used if story is a raw string).
    """
    # 1. Normalize inputs for Algorithmic Analysis
    story_text = (
        extract_story_text(story) if isinstance(story, SocialStorySchema) else story
    )
    age = story.target_age if isinstance(story, SocialStorySchema) else target_age
    # 2. Execute Analysis Tiers
    det_report = deterministic_analysis(story)
    algo_report = algorithmic_analysis(story_text, target_age=age)
    prob_report = probabilistic_analysis(story)
    # 3. Format Report
    lines = [
        "=" * 50,
        "SOCIAL STORY EVALUATION REPORT",
        "=" * 50,
        "",
        "--- TIER 1: DETERMINISTIC CHECKS ---",
        f"  Second Person Pronouns: {'FAIL' if det_report.second_person_pronouns else 'PASS'}",
        f"  Absolute Constraints:   {'FAIL' if det_report.absolute_constraints else 'PASS'}",
        f"  Sentence Ratio:         {'PASS' if det_report.sentence_ratio_criteria else 'FAIL'}",
        f"  TIER 1 STATUS:          {'PASSED' if det_report.tier1_passed else 'FAILED'}",
        "",
        "--- TIER 2: ALGORITHMIC METRICS ---",
        f"  Flesch Reading Ease:    {algo_report.flesch_reading_ease}",
        f"  Flesch-Kincaid Grade:   {algo_report.flesch_kincaid_grade}",
        f"  Dale-Chall Score:       {algo_report.dale_chall_score}",
        f"  Moving Window TTR:      {algo_report.moving_window_ttr}",
        f"  Sentence Length Var:    {algo_report.sentence_length_variance}",
        f"  TIER 2 STATUS:          {'PASSED' if algo_report.tier2_passed else 'FAILED'}",
    ]
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
                f"  TIER 3 STATUS:        {'PASSED' if prob_report.tier3_passed else 'FAILED'}",
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
