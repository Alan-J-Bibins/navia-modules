# Graph Report - navia-modules  (2026-06-03)

## Corpus Check
- 22 files · ~5,225 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 101 nodes · 166 edges · 28 communities (24 shown, 4 thin omitted)
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `699b154d`
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
1. `SocialStorySchema` - 15 edges
2. `call_llm()` - 13 edges
3. `LearnerProfile` - 10 edges
4. `SocialStoryScoreResponse` - 10 edges
5. `str` - 9 edges
6. `create_social_story()` - 8 edges
7. `judge_social_story()` - 7 edges
8. `test_social_story()` - 7 edges
9. `get_learner_profile()` - 6 edges
10. `str` - 6 edges

## Surprising Connections (you probably didn't know these)
- `LearnerProfile` --uses--> `SocialStorySchema`  [INFERRED]
  src/main.py → src/activities/social_story/model.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/main.py → src/activities/social_story/model.py
- `judge_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/judge.py → src/wrappers/text_gen/llm.py
- `test_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/judge.py → src/wrappers/text_gen/llm.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py

## Import Cycles
- None detected.

## Communities (28 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.19
Nodes (18): Caregiver, FamilyMember, FunctionalWordRangeEnum, GenderEnum, LearnerProfile, VerbalAbilityEnum, Enum, LearnerProfile (+10 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.29
Nodes (10): generate_fanar_image(), create_social_story(), create_social_story_schema(), generate_story_visual_plan(), StoryVisualSchema, int, SocialStorySchema, str (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.23
Nodes (17): BaseModel, judge_social_story(), test_social_story(), PageVisualPrompt, SentenceItem, SocialStorySchema, SocialStoryScoreResponse, StoryPage (+9 more)

## Knowledge Gaps
- **4 isolated node(s):** `str`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 10` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `LearnerProfile` connect `Community 0` to `Community 10`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `SocialStorySchema` (e.g. with `LearnerProfile` and `int`) actually correct?**
  _`SocialStorySchema` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `call_llm()` (e.g. with `judge_social_story()` and `test_social_story()`) actually correct?**
  _`call_llm()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `LearnerProfile` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`LearnerProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `int` and `SocialStorySchema`) actually correct?**
  _`SocialStoryScoreResponse` has 8 INFERRED edges - model-reasoned connections that need verification._