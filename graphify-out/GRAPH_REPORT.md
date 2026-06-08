# Graph Report - navia-modules  (2026-06-08)

## Corpus Check
- 32 files · ~8,135 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 144 nodes · 265 edges · 33 communities (28 shown, 5 thin omitted)
- Extraction: 65% EXTRACTED · 35% INFERRED · 0% AMBIGUOUS · INFERRED: 94 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec8e1a7a`
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
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 34|Community 34]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 33 edges
2. `SentenceItem` - 16 edges
3. `call_llm()` - 15 edges
4. `str` - 11 edges
5. `SocialStoryScoreResponse` - 10 edges
6. `evaluate_social_story()` - 9 edges
7. `create_social_story()` - 9 edges
8. `LearnerProfile` - 9 edges
9. `judge_social_story()` - 8 edges
10. `extract_story_text()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `evaluate_social_story()` --calls--> `algorithmic_analysis()`  [INFERRED]
  src/activities/social_story/evaluation/main.py → src/activities/social_story/evaluation/algorithmic_analysis.py
- `SentenceListResponse` --uses--> `SentenceItem`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/activities/social_story/model.py
- `SentenceListResponse` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/activities/social_story/model.py
- `DeterministicAnalysisReport` --uses--> `SentenceItem`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/activities/social_story/model.py
- `DeterministicAnalysisReport` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/activities/social_story/model.py

## Import Cycles
- None detected.

## Communities (33 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (23): generate_social_story_stream(), get_learner_profile(), judge_social_story_handler(), Helper to format SSE events consistently., regenerate_sentence_stream(), sse_event(), create_mock_profile(), bool (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (10): BaseModel, Therapist, annotate_sentences(), deterministic_analysis(), DeterministicAnalysisReport, SentenceListResponse, PageVisualPrompt, StoryPage (+2 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (23): evaluate_social_story(), Aggregates Deterministic, Algorithmic, and Probabilistic analyses into a unified, probabilistic_analysis(), ProbabilisticAnalysisReport, QualitativeMatrix, judge_social_story(), SocialStorySchema, SocialStoryScoreResponse (+15 more)

### Community 30 - "Community 30"
Cohesion: 0.27
Nodes (14): generate_fanar_image(), SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item(), SentenceItem (+6 more)

### Community 34 - "Community 34"
Cohesion: 0.29
Nodes (9): algorithmic_analysis(), AlgorithmicAnalysisReport, calculate_moving_window_ttr(), Calculates the length-agnostic vocabulary repetition rate across a sliding windo, Executes a complete local, deterministic NLP audit on the narrative structure,, # TODO: Dynamically clamp language exposure down based on chronological age limi, float, int (+1 more)

## Knowledge Gaps
- **5 isolated node(s):** `float`, `str`, `str`, `str`, `@opencode-ai/plugin`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 22` to `Community 0`, `Community 3`, `Community 30`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 1` to `Community 3`, `Community 22`, `Community 30`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `evaluate_social_story()` connect `Community 22` to `Community 34`, `Community 3`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `DeterministicAnalysisReport`) actually correct?**
  _`SocialStorySchema` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `SentenceItem` (e.g. with `DeterministicAnalysisReport` and `SentenceListResponse`) actually correct?**
  _`SentenceItem` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `call_llm()` (e.g. with `annotate_sentences()` and `probabilistic_analysis()`) actually correct?**
  _`call_llm()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `str` (e.g. with `Caregiver` and `FamilyMember`) actually correct?**
  _`str` has 7 INFERRED edges - model-reasoned connections that need verification._