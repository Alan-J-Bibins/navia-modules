# Graph Report - navia-modules  (2026-07-09)

## Corpus Check
- 35 files · ~14,621 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 283 nodes · 540 edges · 35 communities (30 shown, 5 thin omitted)
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 165 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `567207a0`
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
1. `SocialStorySchema` - 43 edges
2. `evaluate_social_story_as_dict()` - 19 edges
3. `DeterministicAnalysisReport` - 18 edges
4. `QualitativeMatrix` - 18 edges
5. `ProbabilisticAnalysisReport` - 18 edges
6. `SentenceItem` - 16 edges
7. `ReadabilityAnalysisReport` - 16 edges
8. `evaluate_social_story_as_metrics()` - 16 edges
9. `evaluate_social_story()` - 15 edges
10. `call_llm()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `create_social_story()` --calls--> `generate_fanar_image()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/image_gen/fanar.py
- `generate_image()` --calls--> `comfyui_generate_gemini_image()`  [INFERRED]
  src/wrappers/image_gen/main.py → src/wrappers/image_gen/comfyui/gemini.py
- `annotate_sentences()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/evaluation/deterministic_analysis.py → src/wrappers/text_gen/llm.py
- `probabilistic_analysis()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/evaluation/probabilistic_analysis.py → src/wrappers/text_gen/llm.py
- `create_social_story()` --calls--> `call_llm()`  [INFERRED]
  src/activities/social_story/main.py → src/wrappers/text_gen/llm.py

## Import Cycles
- None detected.

## Communities (35 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (14): comfyui_generate_sdxl_image(), _get_image(), _get_output_image_bytes(), Fetches the generated image bytes from the ComfyUI server., Retrieves the first generated image from ComfyUI history., Generate an image via ComfyUI and save it to disk., generate_fanar_image(), generate_gemini_image() (+6 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (25): 1, class_type, inputs, _meta, 4, class_type, inputs, _meta (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (47): BaseModel, DeterministicAnalysisReport, Therapist, DeterministicAnalysisReport, _build_tier1_factors(), _build_tier2_factors(), _build_tier3_factors(), ComprehensiveReport (+39 more)

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (9): bytes, comfyui_generate_gemini_image(), _get_image(), _get_output_image_bytes(), Fetches the generated image bytes from the ComfyUI server., Retrieves the first generated image from ComfyUI history., Generate an image via Gemini ComfyUI node and save it to disk., bytes (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (42): 1, class_type, inputs, _meta, 2, class_type, _meta, 3 (+34 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (31): annotate_sentences(), deterministic_analysis(), SentenceEntry, SentenceListResponse, SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan() (+23 more)

### Community 30 - "Community 30"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

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

- **Why does `SocialStorySchema` connect `Community 22` to `Community 34`, `Community 3`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 22` to `Community 0`, `Community 34`, `Community 30`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `generate_fanar_image()` connect `Community 0` to `Community 22`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 41 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `DeterministicAnalysisReport`) actually correct?**
  _`SocialStorySchema` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `evaluate_social_story_as_dict()` (e.g. with `deterministic_analysis()` and `probabilistic_analysis()`) actually correct?**
  _`evaluate_social_story_as_dict()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `DeterministicAnalysisReport` (e.g. with `DeterministicAnalysisReport` and `SentenceItem`) actually correct?**
  _`DeterministicAnalysisReport` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `QualitativeMatrix` (e.g. with `DeterministicAnalysisReport` and `ComprehensiveReport`) actually correct?**
  _`QualitativeMatrix` has 15 INFERRED edges - model-reasoned connections that need verification._