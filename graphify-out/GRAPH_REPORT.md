# Graph Report - navia-modules  (2026-06-02)

## Corpus Check
- 21 files · ~5,232 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 109 nodes · 191 edges · 29 communities (24 shown, 5 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 55 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b36faa4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 28|Community 28]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 17 edges
2. `create_social_story()` - 16 edges
3. `SocialStoryScoreResponse` - 15 edges
4. `call_llm()` - 13 edges
5. `LearnerProfile` - 11 edges
6. `str` - 10 edges
7. `test_social_story()` - 9 edges
8. `SocialStorySchema` - 8 edges
9. `generate_html_view()` - 7 edges
10. `get_learner_profile()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `LearnerProfile` --uses--> `SocialStorySchema`  [INFERRED]
  src/main.py → src/social_story/model.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/main.py → src/social_story/model.py
- `int` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/main.py → src/social_story/model.py
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/main.py → src/social_story/model.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/main.py → src/social_story/model.py

## Import Cycles
- None detected.

## Communities (29 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (20): Enum, LearnerProfile, Caregiver, FamilyMember, FunctionalWordRangeEnum, GenderEnum, LearnerProfile, VerbalAbilityEnum (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.28
Nodes (14): create_social_story(), create_social_story_schema(), generate_html_view(), generate_story_image_prompts(), generate_story_visual_plan(), Generates a clean, accessible HTML layout combining imagery and prose blocks., Generates a clean, accessible HTML layout combining imagery and prose blocks., StoryVisualSchema (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.60
Nodes (4): BaseModel, PageVisualPrompt, SentenceItem, StoryPage

### Community 10 - "Community 10"
Cohesion: 0.28
Nodes (14): int, SocialStorySchema, SocialStoryScoreResponse, test_social_story(), save_as_md(), story_text(), SocialStoryScoreResponse, int (+6 more)

## Knowledge Gaps
- **5 isolated node(s):** `str`, `str`, `str`, `@opencode-ai/plugin`, `SocialStoryScoreResponse`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_social_story()` connect `Community 3` to `Community 0`, `Community 1`, `Community 10`, `Community 28`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `SocialStorySchema` connect `Community 10` to `Community 0`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `SocialStorySchema` (e.g. with `int` and `LearnerProfile`) actually correct?**
  _`SocialStorySchema` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `create_social_story()` (e.g. with `generate_fanar_image()` and `test_social_story()`) actually correct?**
  _`create_social_story()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `int` and `int`) actually correct?**
  _`SocialStoryScoreResponse` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `call_llm()` (e.g. with `create_social_story()` and `create_social_story_schema()`) actually correct?**
  _`call_llm()` has 5 INFERRED edges - model-reasoned connections that need verification._