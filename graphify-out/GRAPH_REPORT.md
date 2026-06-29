# Graph Report - navia-modules  (2026-06-29)

## Corpus Check
- 31 files · ~8,864 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 157 nodes · 353 edges · 33 communities (28 shown, 5 thin omitted)
- Extraction: 58% EXTRACTED · 42% INFERRED · 0% AMBIGUOUS · INFERRED: 148 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f94bcbb`
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
1. `SocialStorySchema` - 41 edges
2. `evaluate_social_story_as_dict()` - 17 edges
3. `SentenceItem` - 16 edges
4. `call_llm()` - 15 edges
5. `DeterministicAnalysisReport` - 15 edges
6. `QualitativeMatrix` - 15 edges
7. `ProbabilisticAnalysisReport` - 15 edges
8. `ReadabilityAnalysisReport` - 13 edges
9. `evaluate_social_story()` - 13 edges
10. `str` - 11 edges

## Surprising Connections (you probably didn't know these)
- `annotate_sentences()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/wrappers/text_gen/llm.py
- `probabilistic_analysis()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/evaluation/probabilistic_analysis.py → src/wrappers/text_gen/llm.py
- `judge_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/judge.py → src/wrappers/text_gen/llm.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `create_social_story_schema()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py

## Import Cycles
- None detected.

## Communities (33 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (26): evaluate_social_story_handler(), generate_social_story_stream(), get_learner_profile(), judge_social_story_handler(), Helper to format SSE events consistently., Helper to format SSE events consistently., regenerate_sentence_stream(), sse_event() (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (29): BaseModel, DeterministicAnalysisReport, Therapist, DeterministicAnalysisReport, _compute_tier1_reasons(), _compute_tier2_reasons(), evaluate_social_story(), evaluate_social_story_as_dict() (+21 more)

### Community 10 - "Community 10"
Cohesion: 0.60
Nodes (5): annotate_sentences(), deterministic_analysis(), SentenceListResponse, SocialStorySchema, str

### Community 22 - "Community 22"
Cohesion: 0.24
Nodes (15): probabilistic_analysis(), judge_social_story(), SocialStorySchema, SocialStoryScoreResponse, extract_story_text(), save_as_md(), SocialStorySchema, str (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.19
Nodes (17): generate_fanar_image(), SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item(), PageVisualPrompt (+9 more)

## Knowledge Gaps
- **6 isolated node(s):** `str`, `str`, `str`, `str`, `int` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 22` to `Community 0`, `Community 10`, `Community 3`, `Community 30`?**
  _High betweenness centrality (0.218) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 22`, `Community 30`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `str` connect `Community 0` to `Community 22`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `DeterministicAnalysisReport`) actually correct?**
  _`SocialStorySchema` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `evaluate_social_story_as_dict()` (e.g. with `deterministic_analysis()` and `probabilistic_analysis()`) actually correct?**
  _`evaluate_social_story_as_dict()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `SentenceItem` (e.g. with `DeterministicAnalysisReport` and `SentenceListResponse`) actually correct?**
  _`SentenceItem` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `call_llm()` (e.g. with `annotate_sentences()` and `probabilistic_analysis()`) actually correct?**
  _`call_llm()` has 7 INFERRED edges - model-reasoned connections that need verification._