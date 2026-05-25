from social_story.model import SocialStorySchema

def story_text(story: SocialStorySchema) -> str:
    lines = [f"Title: {story.title}", ""]
    for page in story.pages:
        lines.append(f"Page {page.page_number}:")
        for item in page.sentences:
            lines.append(f"  - {item.text}")
        lines.append("")
    return "\n".join(lines)
