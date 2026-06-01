# Graph Report - navia-modules  (2026-06-01)

## Corpus Check
- 18 files · ~3,902 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 76 nodes · 97 edges · 27 communities (23 shown, 4 thin omitted)
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c472e1af`
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
1. `SocialStorySchema` - 13 edges
2. `SocialStoryScoreResponse` - 13 edges
3. `create_social_story()` - 11 edges
4. `call_llm()` - 8 edges
5. `test_social_story()` - 7 edges
6. `generate_html_view()` - 6 edges
7. `story_text()` - 5 edges
8. `save_as_md()` - 5 edges
9. `SocialStorySchema` - 4 edges
10. `str` - 4 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/test.py → src/social_story/model.py
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/test.py → src/social_story/model.py
- `SocialStoryScoreResponse` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/test.py → src/social_story/model.py
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/utils.py → src/social_story/model.py
- `SocialStoryScoreResponse` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/utils.py → src/social_story/model.py

## Import Cycles
- None detected.

## Communities (27 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.53
Nodes (5): save_as_md(), story_text(), SocialStorySchema, SocialStoryScoreResponse, str

### Community 1 - "Community 1"
Cohesion: 0.71
Nodes (6): str, T, call_deepseek(), call_gemini(), call_gemma(), call_llm()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.26
Nodes (12): int, create_social_story(), generate_html_view(), Generates a clean, accessible HTML layout combining imagery and prose blocks., SocialStorySchema, SocialStorySchema, SocialStoryScoreResponse, int (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.29
Nodes (8): BaseModel, SentenceItem, SocialStoryScoreResponse, StoryPage, test_social_story(), int, SocialStorySchema, SocialStoryScoreResponse

## Knowledge Gaps
- **4 isolated node(s):** `str`, `str`, `@opencode-ai/plugin`, `SocialStoryScoreResponse`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_social_story()` connect `Community 3` to `Community 1`, `Community 10`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `test_social_story()` connect `Community 10` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SocialStorySchema` (e.g. with `int` and `int`) actually correct?**
  _`SocialStorySchema` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `int` and `int`) actually correct?**
  _`SocialStoryScoreResponse` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `create_social_story()` (e.g. with `test_social_story()` and `call_llm()`) actually correct?**
  _`create_social_story()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `call_llm()` (e.g. with `create_social_story()` and `test_social_story()`) actually correct?**
  _`call_llm()` has 2 INFERRED edges - model-reasoned connections that need verification._