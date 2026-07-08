# Graph Report - navia-modules  (2026-07-08)

## Corpus Check
- 35 files · ~13,933 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 269 nodes · 494 edges · 35 communities (30 shown, 5 thin omitted)
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 146 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a02f9cec`
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
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 36|Community 36]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 40 edges
2. `evaluate_social_story_as_dict()` - 18 edges
3. `DeterministicAnalysisReport` - 15 edges
4. `QualitativeMatrix` - 15 edges
5. `ProbabilisticAnalysisReport` - 15 edges
6. `call_llm()` - 14 edges
7. `SentenceItem` - 14 edges
8. `evaluate_social_story()` - 14 edges
9. `ReadabilityAnalysisReport` - 13 edges
10. `str` - 12 edges

## Surprising Connections (you probably didn't know these)
- `SocialStorySchema` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py
- `int` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py
- `str` --uses--> `SentenceItem`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py
- `SentenceItem` --uses--> `SentenceItem`  [INFERRED]
  src/activities/social_story/main.py → src/activities/social_story/model.py

## Import Cycles
- None detected.

## Communities (35 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (8): comfyui_generate_sdxl_image(), _get_image(), _get_output_image_bytes(), Fetches the generated image bytes from the ComfyUI server., Retrieves the first generated image from ComfyUI history., Generate an image via ComfyUI and save it to disk., bytes, str

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (25): 1, class_type, inputs, _meta, 4, class_type, inputs, _meta (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (45): BaseModel, DeterministicAnalysisReport, Therapist, annotate_sentences(), deterministic_analysis(), DeterministicAnalysisReport, SentenceEntry, SentenceListResponse (+37 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (14): bytes, comfyui_generate_gemini_image(), _get_image(), _get_output_image_bytes(), Fetches the generated image bytes from the ComfyUI server., Retrieves the first generated image from ComfyUI history., Generate an image via Gemini ComfyUI node and save it to disk., generate_fanar_image() (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (42): 1, class_type, inputs, _meta, 2, class_type, _meta, 3 (+34 more)

### Community 22 - "Community 22"
Cohesion: 0.24
Nodes (19): int, SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item(), StoryVisualSchema (+11 more)

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (9): PageVisualPrompt, SocialStoryScoreResponse, StoryPage, extract_story_text(), save_as_md(), SocialStoryScoreResponse, SocialStorySchema, SocialStoryScoreResponse (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.14
Nodes (28): evaluate_social_story_handler(), generate_image_handler(), generate_social_story_stream(), get_learner_profile(), Helper to format SSE events consistently., regenerate_sentence_stream(), sse_event(), tier_evaluate_social_story_handler() (+20 more)

### Community 36 - "Community 36"
Cohesion: 0.11
Nodes (19): inputs, inputs, inputs, inputs, cfg, clip, denoise, latent_image (+11 more)

## Knowledge Gaps
- **53 isolated node(s):** `prompt`, `model`, `aspect_ratio`, `image_size`, `file_prefix` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 3` to `Community 34`, `Community 22`, `Community 30`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 22` to `Community 9`, `Community 34`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `generate_fanar_image()` connect `Community 9` to `Community 22`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `DeterministicAnalysisReport`) actually correct?**
  _`SocialStorySchema` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `evaluate_social_story_as_dict()` (e.g. with `deterministic_analysis()` and `probabilistic_analysis()`) actually correct?**
  _`evaluate_social_story_as_dict()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `DeterministicAnalysisReport` (e.g. with `DeterministicAnalysisReport` and `SentenceItem`) actually correct?**
  _`DeterministicAnalysisReport` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `QualitativeMatrix` (e.g. with `DeterministicAnalysisReport` and `EvaluationReportResponse`) actually correct?**
  _`QualitativeMatrix` has 12 INFERRED edges - model-reasoned connections that need verification._