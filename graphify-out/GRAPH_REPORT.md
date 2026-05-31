# Graph Report - navia-modules  (2026-05-31)

## Corpus Check
- 17 files · ~3,825 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 70 nodes · 79 edges · 26 communities (22 shown, 4 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c35d0a8a`
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

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 8 edges
2. `SocialStoryScoreResponse` - 8 edges
3. `call_llm()` - 8 edges
4. `create_social_story()` - 7 edges
5. `test_social_story()` - 6 edges
6. `story_text()` - 5 edges
7. `save_as_md()` - 5 edges
8. `generate_html_view()` - 4 edges
9. `SocialStorySchema` - 4 edges
10. `str` - 4 edges

## Surprising Connections (you probably didn't know these)
- `create_social_story()` --calls--> `test_social_story()`  [INFERRED]
  src/social_story/main.py → src/social_story/test.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/social_story/main.py → src/text_gen/llm.py
- `int` --uses--> `SocialStorySchema`  [INFERRED]
  src/social_story/main.py → src/social_story/model.py
- `int` --uses--> `SocialStoryScoreResponse`  [INFERRED]
  src/social_story/main.py → src/social_story/model.py
- `test_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/social_story/test.py → src/text_gen/llm.py

## Import Cycles
- None detected.

## Communities (26 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (13): BaseModel, SentenceItem, SocialStorySchema, SocialStoryScoreResponse, StoryPage, test_social_story(), save_as_md(), story_text() (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.71
Nodes (6): str, T, call_deepseek(), call_gemini(), call_gemma(), call_llm()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.32
Nodes (7): int, create_social_story(), generate_html_view(), Generates a clean, accessible HTML layout combining imagery and prose blocks., SocialStorySchema, SocialStoryScoreResponse, str

## Knowledge Gaps
- **4 isolated node(s):** `SocialStoryScoreResponse`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_social_story()` connect `Community 3` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `test_social_story()` connect `Community 0` to `Community 1`, `Community 3`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `SocialStorySchema` (e.g. with `int` and `SocialStorySchema`) actually correct?**
  _`SocialStorySchema` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SocialStoryScoreResponse` (e.g. with `int` and `SocialStorySchema`) actually correct?**
  _`SocialStoryScoreResponse` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `call_llm()` (e.g. with `create_social_story()` and `test_social_story()`) actually correct?**
  _`call_llm()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `create_social_story()` (e.g. with `test_social_story()` and `call_llm()`) actually correct?**
  _`create_social_story()` has 2 INFERRED edges - model-reasoned connections that need verification._