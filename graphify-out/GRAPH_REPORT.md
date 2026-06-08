# Graph Report - navia-modules  (2026-06-07)

## Corpus Check
- 26 files · ~6,254 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 118 nodes · 211 edges · 30 communities (26 shown, 4 thin omitted)
- Extraction: 65% EXTRACTED · 35% INFERRED · 0% AMBIGUOUS · INFERRED: 73 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e676d1e4`
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
- [[_COMMUNITY_Community 31|Community 31]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 23 edges
2. `call_llm()` - 13 edges
3. `str` - 11 edges
4. `LearnerProfile` - 10 edges
5. `SocialStoryScoreResponse` - 10 edges
6. `create_social_story()` - 10 edges
7. `LearnerProfile` - 9 edges
8. `StoryVisualSchema` - 8 edges
9. `judge_social_story()` - 8 edges
10. `LearnerProfile` - 7 edges

## Surprising Connections (you probably didn't know these)
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/evaluation_pipeline.py → src/activities/social_story/model.py
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/evaluation_pipeline.py → src/activities/social_story/model.py
- `judge_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/judge.py → src/wrappers/text_gen/llm.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `create_social_story_schema()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py

## Import Cycles
- None detected.

## Communities (30 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (24): generate_social_story_stream(), get_learner_profile(), judge_social_story_handler(), Helper to format SSE events consistently., Helper to format SSE events consistently., Helper to format SSE events consistently., regenerate_sentence_stream(), sse_event() (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.26
Nodes (15): generate_fanar_image(), int, SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item() (+7 more)

### Community 10 - "Community 10"
Cohesion: 0.31
Nodes (12): judge_social_story(), SocialStorySchema, SocialStoryScoreResponse, save_as_md(), story_text(), int, SocialStorySchema, SocialStoryScoreResponse (+4 more)

### Community 31 - "Community 31"
Cohesion: 0.20
Nodes (9): BaseModel, Therapist, deterministic_analysis(), DeterministicAnalysisReport, The idea is to avoid giving the llm deterministic tasks and have it handle quali, PageVisualPrompt, StoryPage, SocialStorySchema (+1 more)

## Knowledge Gaps
- **4 isolated node(s):** `str`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 10` to `Community 0`, `Community 3`, `Community 31`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 3` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `int`) actually correct?**
  _`SocialStorySchema` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `call_llm()` (e.g. with `judge_social_story()` and `create_social_story()`) actually correct?**
  _`call_llm()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `str` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`str` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `LearnerProfile` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`LearnerProfile` has 7 INFERRED edges - model-reasoned connections that need verification._