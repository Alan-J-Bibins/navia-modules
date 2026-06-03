# Graph Report - navia-modules  (2026-06-03)

## Corpus Check
- 21 files · ~5,232 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 98 nodes · 167 edges · 27 communities (23 shown, 4 thin omitted)
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0f14a88a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 16 edges
2. `SocialStoryScoreResponse` - 14 edges
3. `call_llm()` - 12 edges
4. `create_social_story()` - 11 edges
5. `LearnerProfile` - 10 edges
6. `str` - 9 edges
7. `test_social_story()` - 9 edges
8. `StoryVisualSchema` - 6 edges
9. `create_social_story_schema()` - 6 edges
10. `SocialStorySchema` - 6 edges

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

## Communities (27 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.22
Nodes (16): Enum, LearnerProfile, Caregiver, FamilyMember, FunctionalWordRangeEnum, GenderEnum, LearnerProfile, VerbalAbilityEnum (+8 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.30
Nodes (10): generate_fanar_image(), create_social_story(), create_social_story_schema(), generate_story_visual_plan(), StoryVisualSchema, str, int, SocialStorySchema (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (17): BaseModel, PageVisualPrompt, SentenceItem, SocialStorySchema, SocialStoryScoreResponse, StoryPage, test_social_story(), save_as_md() (+9 more)

## Knowledge Gaps
- **4 isolated node(s):** `str`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 10` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 3` to `Community 0`, `Community 1`, `Community 10`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `SocialStorySchema` (e.g. with `LearnerProfile` and `SocialStoryScoreResponse`) actually correct?**
  _`SocialStorySchema` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `SocialStoryScoreResponse` and `int`) actually correct?**
  _`SocialStoryScoreResponse` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `call_llm()` (e.g. with `create_social_story()` and `create_social_story_schema()`) actually correct?**
  _`call_llm()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `create_social_story()` (e.g. with `generate_fanar_image()` and `test_social_story()`) actually correct?**
  _`create_social_story()` has 3 INFERRED edges - model-reasoned connections that need verification._