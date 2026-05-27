# Graph Report - navia-modules  (2026-05-27)

## Corpus Check
- 28 files · ~7,740 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 69 nodes · 84 edges · 27 communities (23 shown, 4 thin omitted)
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b1e47de`
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

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 11 edges
2. `SocialStoryScoreResponse` - 11 edges
3. `call_llm()` - 8 edges
4. `create_social_story()` - 7 edges
5. `test_social_story()` - 6 edges
6. `story_text()` - 5 edges
7. `save_as_md()` - 5 edges
8. `SocialStorySchema` - 4 edges
9. `str` - 4 edges
10. `generate_html_view()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/utils.py → src/social_story/model.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/utils.py → src/social_story/model.py
- `SocialStorySchema` --uses--> `SocialStoryScoreResponse`  [INFERRED]
  src/social_story/utils.py → src/social_story/model.py
- `str` --uses--> `SocialStoryScoreResponse`  [INFERRED]
  src/social_story/utils.py → src/social_story/model.py
- `test_social_story()` --calls--> `story_text()`  [INFERRED]
  src/social_story/test.py → src/social_story/utils.py

## Communities (27 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.26
Nodes (13): int, create_social_story(), generate_html_view(), Generates a clean, accessible HTML layout combining imagery and prose blocks., SocialStorySchema, SocialStoryScoreResponse, test_social_story(), SocialStorySchema (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.71
Nodes (6): str, T, call_deepseek(), call_gemini(), call_gemma(), call_llm()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.70
Nodes (4): save_as_md(), story_text(), SocialStorySchema, str

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (3): BaseModel, SentenceItem, StoryPage

## Knowledge Gaps
- **3 isolated node(s):** `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `call_llm()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `test_social_story()` connect `Community 0` to `Community 1`, `Community 3`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `SocialStorySchema` (e.g. with `SocialStorySchema` and `str`) actually correct?**
  _`SocialStorySchema` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `SocialStorySchema` and `str`) actually correct?**
  _`SocialStoryScoreResponse` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `call_llm()` (e.g. with `create_social_story()` and `test_social_story()`) actually correct?**
  _`call_llm()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `create_social_story()` (e.g. with `call_llm()` and `test_social_story()`) actually correct?**
  _`create_social_story()` has 2 INFERRED edges - model-reasoned connections that need verification._