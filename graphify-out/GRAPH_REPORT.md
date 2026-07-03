# Graph Report - navia-modules  (2026-07-03)

## Corpus Check
- 30 files · ~8,057 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 158 nodes · 359 edges · 35 communities (30 shown, 5 thin omitted)
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `28da7908`
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
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 34|Community 34]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 39 edges
2. `evaluate_social_story_as_dict()` - 18 edges
3. `SentenceItem` - 16 edges
4. `DeterministicAnalysisReport` - 15 edges
5. `QualitativeMatrix` - 15 edges
6. `ProbabilisticAnalysisReport` - 15 edges
7. `call_llm()` - 14 edges
8. `evaluate_social_story()` - 14 edges
9. `ReadabilityAnalysisReport` - 13 edges
10. `str` - 11 edges

## Surprising Connections (you probably didn't know these)
- `annotate_sentences()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/wrappers/text_gen/llm.py
- `probabilistic_analysis()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/evaluation/probabilistic_analysis.py → src/wrappers/text_gen/llm.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `create_social_story_schema()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py
- `generate_story_visual_plan()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py

## Import Cycles
- None detected.

## Communities (35 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.26
Nodes (14): get_learner_profile(), Helper to format SSE events consistently., Helper to format SSE events consistently., sse_event(), create_mock_profile(), Caregiver, FamilyMember, FunctionalWordRangeEnum (+6 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (22): _compute_tier1_reasons(), _compute_tier2_reasons(), evaluate_social_story(), evaluate_social_story_as_dict(), evaluate_social_story_as_metrics(), _get_age_thresholds(), Aggregates Deterministic, Algorithmic (Readability), and Probabilistic analyses, Aggregates Deterministic, Algorithmic (Readability), and Probabilistic analyses (+14 more)

### Community 10 - "Community 10"
Cohesion: 0.52
Nodes (6): annotate_sentences(), deterministic_analysis(), SentenceEntry, SentenceListResponse, SocialStorySchema, str

### Community 22 - "Community 22"
Cohesion: 0.46
Nodes (7): SocialStoryScoreResponse, extract_story_text(), save_as_md(), SocialStoryScoreResponse, SocialStorySchema, SocialStoryScoreResponse, str

### Community 30 - "Community 30"
Cohesion: 0.22
Nodes (16): generate_fanar_image(), SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item(), PageVisualPrompt (+8 more)

### Community 32 - "Community 32"
Cohesion: 0.35
Nodes (16): BaseModel, DeterministicAnalysisReport, Therapist, DeterministicAnalysisReport, EvaluationReportResponse, Tier1Result, Tier2Result, Tier3Result (+8 more)

### Community 34 - "Community 34"
Cohesion: 0.31
Nodes (13): evaluate_social_story_handler(), generate_social_story_stream(), judge_social_story_handler(), regenerate_sentence_stream(), tier_evaluate_social_story_handler(), bool, LearnerProfile, LearnerProfile (+5 more)

## Knowledge Gaps
- **6 isolated node(s):** `str`, `str`, `str`, `str`, `int` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 32` to `Community 0`, `Community 34`, `Community 3`, `Community 10`, `Community 22`, `Community 30`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 10`, `Community 3`, `Community 30`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `str` connect `Community 0` to `Community 32`, `Community 34`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `DeterministicAnalysisReport`) actually correct?**
  _`SocialStorySchema` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `evaluate_social_story_as_dict()` (e.g. with `deterministic_analysis()` and `probabilistic_analysis()`) actually correct?**
  _`evaluate_social_story_as_dict()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `SentenceItem` (e.g. with `DeterministicAnalysisReport` and `SentenceListResponse`) actually correct?**
  _`SentenceItem` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `DeterministicAnalysisReport` (e.g. with `DeterministicAnalysisReport` and `SentenceItem`) actually correct?**
  _`DeterministicAnalysisReport` has 12 INFERRED edges - model-reasoned connections that need verification._