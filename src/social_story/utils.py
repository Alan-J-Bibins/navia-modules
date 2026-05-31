from social_story.model import SocialStorySchema, SocialStoryScoreResponse


def story_text(story: SocialStorySchema) -> str:
    lines = [f"Title: {story.title}", ""]
    for page in story.pages:
        lines.append(f"Page {page.page_number}:")
        for item in page.sentences:
            lines.append(f"  - {item.text}")
        lines.append("")
    return "\n".join(lines)


def save_as_md(
    story_schema: SocialStorySchema,
    story_report: SocialStoryScoreResponse,
    filename: str,
):
    md_lines = [
        story_text(story_schema),
        "\n---\n",
        f"**Score:** {story_report.score}/100\n",
        "**Remarks:**\n",
        *story_report.remarks,
        ""
    ]
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Saved {filename}")
