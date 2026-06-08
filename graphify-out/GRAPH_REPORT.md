# Graph Report - navia-modules  (2026-06-08)

## Corpus Check
- 26 files · ~6,254 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 113 nodes · 195 edges · 32 communities (27 shown, 5 thin omitted)
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `016dc9d9`
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
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 21 edges
2. `call_llm()` - 13 edges
3. `str` - 11 edges
4. `SocialStoryScoreResponse` - 10 edges
5. `create_social_story()` - 9 edges
6. `LearnerProfile` - 8 edges
7. `judge_social_story()` - 8 edges
8. `SentenceItem` - 7 edges
9. `StoryVisualSchema` - 7 edges
10. `LearnerProfile` - 7 edges

## Surprising Connections (you probably didn't know these)
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/evaluation_pipeline.py → src/activities/social_story/model.py
- `regenerate_sentence_item()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py
- `int` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py

## Import Cycles
- None detected.

## Communities (32 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (13): generate_social_story_stream(), get_learner_profile(), judge_social_story_handler(), Helper to format SSE events consistently., regenerate_sentence_stream(), sse_event(), bool, LearnerProfile (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.23
Nodes (16): BaseModel, Therapist, SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item() (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.31
Nodes (12): judge_social_story(), SocialStorySchema, SocialStoryScoreResponse, save_as_md(), story_text(), int, SocialStorySchema, SocialStoryScoreResponse (+4 more)

### Community 22 - "Community 22"
Cohesion: 0.38
Nodes (9): create_mock_profile(), Caregiver, FamilyMember, FunctionalWordRangeEnum, GenderEnum, VerbalAbilityEnum, Enum, LearnerProfile (+1 more)

### Community 31 - "Community 31"
Cohesion: 0.67
Nodes (3): deterministic_analysis(), DeterministicAnalysisReport, str

## Knowledge Gaps
- **4 isolated node(s):** `str`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 10` to `Community 0`, `Community 3`, `Community 31`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 3` to `Community 1`, `Community 30`, `Community 22`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `LearnerProfile`) actually correct?**
  _`SocialStorySchema` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `call_llm()` (e.g. with `judge_social_story()` and `create_social_story()`) actually correct?**
  _`call_llm()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `str` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`str` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `int` and `SocialStorySchema`) actually correct?**
  _`SocialStoryScoreResponse` has 8 INFERRED edges - model-reasoned connections that need verification._