# Graph Report - navia-modules  (2026-06-04)

## Corpus Check
- 25 files · ~5,284 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 118 nodes · 203 edges · 31 communities (27 shown, 4 thin omitted)
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 68 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0fcc249`
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

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 19 edges
2. `call_llm()` - 12 edges
3. `LearnerProfile` - 11 edges
4. `str` - 10 edges
5. `SocialStoryScoreResponse` - 10 edges
6. `LearnerProfile` - 10 edges
7. `LearnerProfile` - 9 edges
8. `create_social_story()` - 9 edges
9. `get_learner_profile()` - 8 edges
10. `FamilyMember` - 8 edges

## Surprising Connections (you probably didn't know these)
- `judge_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/judge.py → src/wrappers/text_gen/llm.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `create_social_story_schema()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `generate_story_visual_plan()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/api/main.py → src/activities/social_story/model.py

## Import Cycles
- None detected.

## Communities (31 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (21): _create_mock_profile(), generate_social_story_stream(), get_learner_profile(), Dependency to inject the mock profile into any route., Dependency to inject the mock profile into any route., Dependency to inject the mock profile into any route., create_mock_profile(), bool (+13 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.29
Nodes (10): generate_fanar_image(), create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), StoryVisualSchema, int, SocialStorySchema (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.24
Nodes (15): judge_social_story_handler(), judge_social_story(), SocialStorySchema, SocialStoryScoreResponse, save_as_md(), story_text(), int, SocialStorySchema (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.20
Nodes (7): mock_login(), Create a mock session and return a session token., Create a mock session and return a session token., Create a mock session and return a session token., Helper to format SSE events consistently., Helper to format SSE events consistently., sse_event()

### Community 30 - "Community 30"
Cohesion: 0.36
Nodes (6): BaseModel, Therapist, Therpist, PageVisualPrompt, SentenceItem, StoryPage

## Knowledge Gaps
- **4 isolated node(s):** `str`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 10` to `Community 0`, `Community 3`, `Community 30`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `judge_social_story()` connect `Community 10` to `Community 1`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `LearnerProfile`) actually correct?**
  _`SocialStorySchema` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `call_llm()` (e.g. with `judge_social_story()` and `create_social_story()`) actually correct?**
  _`call_llm()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `LearnerProfile` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`LearnerProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `str` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`str` has 7 INFERRED edges - model-reasoned connections that need verification._