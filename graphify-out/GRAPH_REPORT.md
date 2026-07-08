# Graph Report - navia-modules  (2026-07-07)

## Corpus Check
- 33 files · ~11,257 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 238 nodes · 451 edges · 35 communities (30 shown, 5 thin omitted)
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 141 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1f7a28fa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
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
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]

## God Nodes (most connected - your core abstractions)
1. `SocialStorySchema` - 36 edges
2. `evaluate_social_story_as_dict()` - 18 edges
3. `SentenceItem` - 16 edges
4. `DeterministicAnalysisReport` - 15 edges
5. `QualitativeMatrix` - 15 edges
6. `ProbabilisticAnalysisReport` - 15 edges
7. `call_llm()` - 14 edges
8. `evaluate_social_story()` - 14 edges
9. `ReadabilityAnalysisReport` - 13 edges
10. `str` - 12 edges

## Surprising Connections (you probably didn't know these)
- `str` --uses--> `SocialStorySchema`  [INFERRED]
  src/api/main.py → src/activities/social_story/model.py
- `Request` --uses--> `SocialStorySchema`  [INFERRED]
  src/api/main.py → src/activities/social_story/model.py
- `LearnerProfile` --uses--> `SocialStorySchema`  [INFERRED]
  src/api/main.py → src/activities/social_story/model.py
- `bool` --uses--> `SocialStorySchema`  [INFERRED]
  src/api/main.py → src/activities/social_story/model.py
- `UploadFile` --uses--> `SocialStorySchema`  [INFERRED]
  src/api/main.py → src/activities/social_story/model.py

## Import Cycles
- None detected.

## Communities (35 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (20): bytes, generate_comfyui_image(), _get_image(), _get_output_image_bytes(), _queue_prompt(), Fetches the generated image bytes from the ComfyUI server., Sends the execution payload to ComfyUI., Retrieves the first generated image from ComfyUI history. (+12 more)

### Community 2 - "Community 2"
Cohesion: 0.80
Nodes (4): generate_lightning_image(), generate_with_image_continuity(), sdxl_create_image(), str

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (38): BaseModel, DeterministicAnalysisReport, Therapist, DeterministicAnalysisReport, _compute_tier1_reasons(), _compute_tier2_reasons(), evaluate_social_story(), evaluate_social_story_as_dict() (+30 more)

### Community 9 - "Community 9"
Cohesion: 0.64
Nodes (8): str, T, call_deepseek(), call_fanar(), call_gemini(), call_gemma(), call_llm(), call_qwen3dot6()

### Community 10 - "Community 10"
Cohesion: 0.52
Nodes (6): annotate_sentences(), deterministic_analysis(), SentenceEntry, SentenceListResponse, SocialStorySchema, str

### Community 22 - "Community 22"
Cohesion: 0.46
Nodes (7): SocialStoryScoreResponse, extract_story_text(), save_as_md(), SocialStoryScoreResponse, SocialStorySchema, SocialStoryScoreResponse, str

### Community 30 - "Community 30"
Cohesion: 0.28
Nodes (14): SentenceItem, create_social_story(), create_social_story_schema(), generate_story_visual_plan(), main(), regenerate_sentence_item(), PageVisualPrompt, SentenceItem (+6 more)

### Community 32 - "Community 32"
Cohesion: 0.06
Nodes (42): 1, class_type, inputs, _meta, 2, class_type, _meta, 3 (+34 more)

### Community 34 - "Community 34"
Cohesion: 0.15
Nodes (26): evaluate_social_story_handler(), generate_image_handler(), generate_social_story_stream(), get_learner_profile(), Helper to format SSE events consistently., regenerate_sentence_stream(), sse_event(), tier_evaluate_social_story_handler() (+18 more)

### Community 35 - "Community 35"
Cohesion: 0.11
Nodes (19): inputs, inputs, inputs, inputs, cfg, clip, denoise, latent_image (+11 more)

## Knowledge Gaps
- **39 isolated node(s):** `int`, `str`, `str`, `ckpt_name`, `class_type` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialStorySchema` connect `Community 3` to `Community 34`, `Community 10`, `Community 30`, `Community 22`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `create_social_story()` connect `Community 30` to `Community 0`, `Community 9`, `Community 34`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `generate_fanar_image()` connect `Community 0` to `Community 30`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `SocialStorySchema` (e.g. with `bool` and `DeterministicAnalysisReport`) actually correct?**
  _`SocialStorySchema` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `evaluate_social_story_as_dict()` (e.g. with `deterministic_analysis()` and `probabilistic_analysis()`) actually correct?**
  _`evaluate_social_story_as_dict()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `SentenceItem` (e.g. with `DeterministicAnalysisReport` and `SentenceListResponse`) actually correct?**
  _`SentenceItem` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `DeterministicAnalysisReport` (e.g. with `DeterministicAnalysisReport` and `SentenceItem`) actually correct?**
  _`DeterministicAnalysisReport` has 12 INFERRED edges - model-reasoned connections that need verification._