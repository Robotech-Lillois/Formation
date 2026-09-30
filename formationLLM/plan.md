# Plan de formation — "Des LLM aux agents locaux" (2 h)

**Draft plan for a quick 2-hour lecture: from explaining LLMs → running local models (llama.cpp) → harnesses (DeepSeek Harness).**
Target: get the uninitiated up to speed. Companion deck skeleton: [formation_llm.tex](./formation_llm.tex) (same Beamer form as `~/polytech/robotech/Formation/Git/formation_git.tex`).

> **Language decision**: plan written in English (for you); the deck skeleton is written in **French**, matching the existing `formation_git.tex` template and the Robotech audience. Flip if the audience changes.
>
> **Freshness warning**: the local-AI/harness world moves fast. Everything below was verified with live web searches on **2026-09-29** (model names, versions, flags below reflect that date). Re-verify the items in [§9 Verify-before-teaching](#9-verify-before-teaching-checklist) on the day of the lecture.

---

## 1. Goal & audience

- **Audience**: Robotech club students (same as the Git formation). Comfortable with a terminal and Git, **no ML background assumed**.
- **Duration**: 120 min, front + 2 live demos + 1 short exercise.
- **One-sentence thesis to repeat all along**: an LLM is a next-token predictor; everything else (chat, tools, agents) is software around it — *agent = model + harness* ([Wikipedia: Agent harness](https://en.wikipedia.org/wiki/Agent_harness)).

### Learning objectives (say these on slide 3)
1. Explain what happens inside an LLM when it "talks" (tokens → embeddings → attention → next token).
2. Explain why size/quantization/context decide what runs on **your** machine, and run a GGUF model locally with llama.cpp.
3. Explain the difference between a chat loop and an **agent loop**, and connect a local model to an agent harness (DeepSeek Harness `dsh`).

### Prerequisites to state up front
- Command line basics (the Git formation is enough).
- No math beyond "vectors and dot products" (used intuitively).

---

## 2. Format & materials (follows the Git formation repo)

| Item | Choice |
|---|---|
| Form | Beamer, `CambridgeUS`, miniframes, 11pt, 16:9, Open Sans — copied from `formation_git.tex` preamble (theme, headline with dots + logo, footline, `fragile` frames, listings style) |
| Palette | New `llmblue` (#4D6BFE DeepSeek-ish) + dark slate + green/red accents; `block`/`exampleblock`/`alertblock` used like the Git deck |
| Sections | Sommaire → Introduction → Comprendre un LLM → Faire tourner un modèle → Harnais d'agents → Exercice → Conclusion (mirrors Git deck's Introduction → Philosophie → Bases → Setup → Exercice → Conclusion rhythm) |
| Images | 24 figures downloaded from the [3Blue1Brown attention lesson](https://www.3blue1brown.com/lessons/attention) into [`img/`](./img/) — mapping in §4.2; attribution in [img/README.md](./img/README.md) |
| Demos | [`demo/demo_llama.sh`](./demo/demo_llama.sh) (llama.cpp) + [`demo/dsh-provider-example.yaml`](./demo/dsh-provider-example.yaml) (dsh ↔ llama-server) |
| Build | [Makefile](./Makefile) with `latexmk` (copied from Git repo, `SRC = ./formation_llm.tex`) |
| Licence | CC BY-NC-SA 4.0 like the Git deck |

---

## 3. Minute-by-minute run-of-show (120 min)

| Time | Block | Frames | Key artifact |
|---|---|---|---|
| 0–10 | **Introduction**: why local, map of the stack | 4 | "model / runner / interface / harness" diagram |
| 10–48 | **Part 1 — Comprendre un LLM** (3b1b core) | ~16 | attention sequence with Q/K/V figures |
| 48–53 | *Mini-pause / questions* | — | — |
| 53–80 | **Part 2 — Faire tourner un modèle (llama.cpp)** | ~10 | **Demo A**: `llama cli -hf`, `llama-server` web UI |
| 80–107 | **Part 3 — Harnais d'agents (DeepSeek Harness)** | ~12 | **Demo B**: `llama-server --jinja` + `dsh web` local provider |
| 107–117 | **Exercice**: sizing a model for your laptop | 2 + worksheet | sizing table + answer key |
| 117–120 | **Conclusion** + resources | 2 | recap takeaways à la Git deck |

---

## 4. Section-by-section content (what to say, which figure)

### 4.1 Introduction (10 min)
- **"What you will be able to do in 2 h"**: run `Qwen3.5-0.8B-GGUF` on any laptop; explain attention to a friend; connect a local model to an agent.
- **Why local?** privacy, zero marginal cost, offline/demos, learning & control, no rate limits. Why cloud? raw capability, no hardware. Not a religion — a trade-off slide.
- **Map of the stack** (draw as TikZ or reuse later as recurring figure):
  `model (weights, GGUF) → runner (llama.cpp / Ollama / LM Studio / vLLM) → interface (CLI / OpenAI-compatible API / Web UI) → harness (dsh, Claude Code, Codex…)`
  Punchline: "Ollama and LM Studio *are* llama.cpp underneath — same model + quant + GPU ⇒ speed differences are wrapper overhead." ([inventivehq](https://inventivehq.com/blog/ollama-vs-lm-studio-vs-llama-cpp))
- Announce the two demos and the exercise.

### 4.2 Part 1 — Comprendre un LLM (38 min) — 3Blue1Brown-based
All figures listed are in [`img/`](./img/), downloaded from [3b1b's attention lesson](https://www.3blue1brown.com/lessons/attention) (Deep Learning Chapter 6).

| # | Slide | Content | Figure |
|---|---|---|---|
| 1 | Next-token prediction | Goal: predict the next token. Text → **tokens** (often word *pieces*, not words) → model | (tokenization slide, own TikZ) |
| 2 | Embeddings | Each token → high-dimensional vector; **directions encode meaning** (gender example from ch.5) | `Embeddings.jpg` |
| 3 | Problem: context | "mole" in *American shrew mole / one mole of CO₂ / biopsy of the mole* — same embedding before attention | `MoleExample.jpg` |
| 4 | Tower example | *tower* + *Eiffel* → Paris/iron; + *miniature* → not tall. Info transfers across large distances | `TowerExample.jpg` |
| 5 | The last vector | "Therefore the murderer was…" — final vector must encode the whole context window | `lastvector.jpg` |
| 6 | Attention = Q, K, V | Each token asks questions (`W_Q`·E = **query**); keys = potential answers (`W_K`·E); dot product = alignment score | `SingleHead.jpg`, `W_Q.jpg`, `QueryKey.jpg`, `Keys.jpg`, `DotProduct.jpg` |
| 7 | Update | **Value** vectors from neighbors, mixed by relevance, added to the token's vector → refined meaning | `ValueVector.jpg`, `ValueQueryKey.jpg`, `DeltaE.jpg`, `added.jpg` |
| 8 | Multi-head | 96 heads in GPT-3, each its own Q/K/V → many "ways context changes meaning" in parallel | `MultiHeaded.jpg`, `Harry.jpg` |
| 9 | Many blocks | Attention + MLP repeated 96× (GPT-3); deeper = more abstract (sentiment, tone…) | `ManyBlocks.jpg` |
| 10 | Parameter count | ~6.3M params/head; ~600M per block; attention ≈ 58B ≈ **⅓ of GPT-3's 175B** — "even though attention gets all the attention" | `CountQueryKey.jpg`, `ParameterCount2.jpg`, `FinalCount.jpg` |
| 11 | Why context is expensive | Every token can interact with every other ⇒ doubling context quadruples the work; KV cache stores K,V per token ⇒ RAM cost of long context | `square.jpg` |
| 12 | Generation | Prefill (parallel, fast) vs decode (one token at a time, memory-bound) ⇒ the `tok/s` you see in llama.cpp; sampling/temperature = dice on the word ranking | (own slide) |
| 14 | What it is *not* | Not a database; hallucination = plausible continuation, not retrieval; no memory between calls (setup for Part 3: *that's why a harness exists*) | (own slide) |
| 15 | Why scale works | Attention is massively **parallelizable** on GPUs → scale alone gives qualitative jumps (3b1b closing point) | (own slide) |

> Pedagogical note: keep 3b1b's "made-up example" caveat ("adjectives updating nouns is a plausibility illustration, the real maps are learned and hard to interpret") — the audience will otherwise over-interpret.

### 4.3 Part 2 — Faire tourner un modèle (27 min)
- **From weights to GGUF**: [llama.cpp](https://github.com/ggml-org/llama.cpp) (ggml-org, MIT, ~130k stars): "LLM inference in C/C++ with minimal setup and state-of-the-art performance on a wide range of hardware". GGUF = container format (weights + tokenizer + chat template).
- **Quantization** (from the 3b1b "size" thread to bits/weight): 1.5–8-bit integer quantization is core to the project ([README](https://github.com/ggml-org/llama.cpp)). Slide table:

  | Scheme | bits/weight (≈) | Use |
  |---|---|---|
  | Q8_0 | ~8.5 | near-lossless, big |
  | **Q4_K_M** | ~4.8 | **recommended default** — most of Q8 quality at ~½ size (llama.cpp reference data, [markaicode benchmark](https://markaicode.com/benchmarks/llamacpp-inference-benchmark/)) |
  | Q3_K_M / Q2 | ~3 / ~2.5 | last resort, quality drops fast |
- **Hardware rules of thumb** ([ComputingForGeeks lab](https://computingforgeeks.com/deepseek-harness-local-model/), [localllm.in VRAM guide](https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms)):
  - `weights ≈ #params × bits/weight` → 8B @ Q4 ≈ 5 GB; 4B fp16 ≈ 8 GB.
  - **KV cache for the context is on top** — agents build long prompts; budget it (Qwen3.5-35B Q4_K_M ≈ 21.6 GB *with* 32K ctx ⇒ fits 3090/4090).
  - Backends: Metal (Apple Silicon first-class), CUDA, Vulkan, HIP, CPU (AVX/NEON); **CPU+GPU hybrid offloading** when the model doesn't fit ([README](https://github.com/ggml-org/llama.cpp)).
  - Reality check: CPU-only is fine for chat, *bad* for agents (lab measured 2.23 tok/s on a weak CPU build; an agent turn never finished in 300 s because the harness resends ~25 tool schemas each step).
- **Model zoo (Sept 2026 landscape)**: Hugging Face; Unsloth "Dynamic GGUF" repos; current families: **Qwen3.5** (0.8B → 35B+), **Qwen3.8-Flash-Next** (the quantized GGUF *this* session runs on!), Gemma 4 (QAT variants), MoE models need expert offloading to be practical ([pinggy roundup](https://pinggy.io/blog/top_5_local_llm_tools_and_models/), [kdnuggets](https://www.kdnuggets.com/top-7-coding-models-you-can-run-locally-in-2026), [maksim lin](https://medium.com/@mksl/what-can-a-local-model-do-for-you-early-sept-2026-edition-ba9dadf05d74)).
- **Tooling** (keep it to 3 commands):
  - `llama cli -hf ggml-org/Qwen3.5-0.8B-GGUF` — chat in terminal straight from HF ([README quick start](https://github.com/ggml-org/llama.cpp))
  - `llama-server -hf … --jinja -c 8192` — OpenAI-compatible API **and built-in web UI**
  - `llama benchmark` / status line: explain tok/s, prefill vs decode.
- **🎬 Demo A** (see [demo/demo_llama.sh](./demo/demo_llama.sh)): run 0.8B live (seconds), show tok/s line, then `llama-server` web UI in the room browser. Optional: same question on Q4 vs Q8 to show size/quality trade-off.

### 4.4 Part 3 — Harnais d'agents (27 min)
- **Chat loop vs agent loop**: chat = 1 request → 1 answer. Agent = loop *think → act (tool call) → observe → repeat* (ReAct idea, 2023; tools first demoed by Toolformer — [agent harness overview](https://en.wikipedia.org/wiki/Agent_harness)).
- **Function calling**: the runner advertises tool JSON schemas; the model *emits a structured call*; the harness executes it and feeds back the result. llama.cpp needs `--jinja` for OpenAI-shaped tool calls — "without it, an agent is a chatbot" ([lab article](https://computingforgeeks.com/deepseek-harness-local-model/)).
- **Definition**: `agent = model + harness`. The harness manages tool dispatch, memory/state, sandbox/workspace, **context management**, guardrails (permissions, approvals) ([Wikipedia](https://en.wikipedia.org/wiki/Agent_harness)).
- **Inner vs outer harness** (Böckeler, martinfowler.com): inner = shipped by the builder (SDK, dsh, Claude Code); outer = what *you* assemble: `AGENTS.md` instruction files, MCP servers, custom skills. **Guides** (steer before acting: instructions, skills) vs **sensors** (observe after: linters, tests, LLM-as-judge).
- **Context engineering, visible costs**: system prompt + tool catalog ride on **every** request — 25 tool schemas ≈ 14.7K input tokens to read a 3-line CSV ([lab article](https://computingforgeeks.com/deepseek-harness-local-model/)). Hence: context window = money/RAM; harnesses compact/trim context (this very deck's author session uses compression). Server-side `-c` must match the harness's declared `contextWindow` or you get *silent* context-shift truncation.
- **MCP** = standardized plug for tools; **skills** = SKILL.md folders; everything is discoverable, local, file-based.
- **DeepSeek Harness (dsh)** ([repo](https://github.com/deepseek-ai/deepseek-harness), MIT, developer preview, "everything is a plugin", powered by Cordis): start with `npx @deepseek-ai/dsh web` → Web UI at `http://127.0.0.1:3080`. Add a **custom model API** in Settings → Models (provider id, base URL, protocol `openai-completions`, placeholder key, model id + context window) — or edit the profile config (`cordis.patch.yml`; older builds: `~/.dsh/settings.yaml`) ([providers guide](https://deepseek-harness.github.io/deepseek-harness/en/guide/providers)).
  Compat switches that save local integrations: `supportsDeveloperRole: false`, `maxTokensField: max_tokens` ([providers guide](https://deepseek-harness.github.io/deepseek-harness/en/guide/providers)).
  Credential trap: a route **must** resolve a credential — `apiKeyEnv: DSH_LLM_KEY` + `export DSH_LLM_KEY=local` (server ignores it, but the adapter won't send without it).
- **🐧 Installer dsh sur Debian** (2 slides, avant Démo B) : Node trop vieux → NodeSource (`setup_22.x`), dsh exige Node ≥ 22.19 (Node 23 exclu) ; install globale `npm install -g @deepseek-ai/dsh` (option à `npx`) ; télémétrie à désactiver dans `~/.dsh/profiles/web/cordis.patch.yml` (`mode: DISABLED`).
- **🎬 Demo B** (see [demo/dsh-provider-example.yaml](./demo/dsh-provider-example.yaml)): `llama-server --jinja -c 16384` on port 8080 + `dsh web` pointed at it; task "read parts.csv, total quantity" → show tool call in the UI, then open `llama-server`'s log to show the 10K+-token prompt. *Fallback*: if the local model is too weak live, switch the same session to the hosted DeepSeek API and show the identical harness.
- **Safety slide**: approvals & sandboxing, prompt injection, "the wrapped thing is non-deterministic — design for recovery" ([Wikipedia](https://en.wikipedia.org/wiki/Agent_harness)).

### 4.5 Exercice (10 min) — "Size it before you run it"
Worksheet (project instructions; 5 min solo, 5 min debrief):
For three machines choose **model + quant + context** and justify in one line each:
1. Old laptop: 16 GB RAM, **no GPU**
2. Gaming PC: RTX 3060 12 GB + 32 GB RAM
3. MacBook Air M1: 8 GB unified

Answer key (approx): 1) Qwen3.5-0.8B/4B Q4_K_M, small ctx, chat only (agents painful); 2) Qwen3.5-8B/9B Q4_K_M full in VRAM (+KV for 8–16K), or MoE partially offloaded; 3) 3–4B Q4 (~3–4 GB) + KV budget, Metal backend. Rule repeated: `params × bits + KV ≤ available`, KV grows with context.
Optional homework (script in `demo/`): run Demo A/B on your own machine and report tok/s + which model you can *actually* use for agents.

### 4.6 Conclusion (3 min)
Git-deck-style recap bullets:
- **Next-token prediction + attention** explains both the magic and the limits (context², hallucinations).
- **Local is a budget problem**: params × bits + KV cache ≤ your RAM/VRAM → pick quant accordingly (Q4_K_M default).
- **agent = model + harness**: tools, state, context management, guardrails — llama.cpp runs the model, dsh runs the agent.
- **Same protocol everywhere** (OpenAI-compatible API) ⇒ any runner + any harness compose freely.
- Merci + CC BY-NC-SA + resources: 3b1b attention lesson, Karpathy "Let's build GPT", llama.cpp docs (llama.app), dsh docs, r/LocalLLaMA.

---

## 5. Demo scripts (exact commands, verified against Sept 2026 sources)

Full files: [demo/demo_llama.sh](./demo/demo_llama.sh), [demo/dsh-provider-example.yaml](./demo/dsh-provider-example.yaml).

```bash
# ---- Demo A: chat + server ----
llama cli -hf ggml-org/Qwen3.5-0.8B-GGUF                 # terminal chat, downloads from HF
llama-server -hf ggml-org/Qwen3.5-0.8B-GGUF \
  --host 127.0.0.1 --port 8080 -c 8192 --jinja           # API + built-in web UI
# NixOS alternative: nix shell nixpkgs#llama-cpp --command sh -c '...' (verify attribute w/ nix MCP)

# ---- Demo B: harness on the local model ----
npx @deepseek-ai/dsh web                                  # Web UI at http://127.0.0.1:3080
# Settings → Models → "Add a custom model API":
#   provider id: local   api: OpenAI Chat Completions   baseURL: http://127.0.0.1:8080/v1
#   model id: ggml-org/Qwen3.5-0.8B-GGUF   contextWindow: 8192   key: "local" (ignored by server)
```

Known traps to mention (they are lecture content, not just ops):
- **`--jinja` required** for OpenAI-shaped tool calls in llama-server.
- **Context mismatch**: harness `contextWindow` vs server `-c`: overflow ⇒ silent context-shift truncation (or hard error on some archs). Grep journal for "truncating input prompt".
- **Model id must match exactly** what `curl /v1/models` advertises (GGUF repos: `org/repo:QUANT` form for some runners).
- **dsh needs Node ≥ 22.19 (22.x) or ≥ 24; Node 23 excluded** ([lab article](https://computingforgeeks.com/deepseek-harness-local-model/)).
- CPU-only llama.cpp = chat OK, agent turns time out (tool schemas resent every step).

## 6. Preparation checklist

**T-7 days**: pick demo machine (GPU if possible); pre-download all GGUFs (venue Wi-Fi is the classic killer); rehearse both demos end-to-end *with the deck*; decide hosted-API fallback credentials.
**T-1 day**: compile the deck (`make`); `git clone` a fresh demo dir; freeze llama.cpp build (releases are per-build tags `bNNNN` — the `latest` endpoint lies, use releases list first entry); test `npx @deepseek-ai/dsh web` on the venue machine.
**Day of**: offline copies in `~/dsh-work/` and GGUF cache; record a 60-s screen capture of Demo B as Plan C; check Node version; projector browser at `127.0.0.1:3080`.

## 7. Risks & fallbacks

| Risk | Mitigation |
|---|---|
| Venue has no GPU / slow CPU | 0.8B model for Demo A; hosted-DeepSeek fallback for Demo B (identical harness UX) |
| Download blocked at venue | all GGUFs pre-cached (§6); `-hf` works offline once cached |
| dsh developer-preview breaking change (README: "THERE WILL BE COMPATIBILITY-BREAKING CHANGES") | pin a version that worked at rehearsal; re-check docs §9 |
| Attention section too dense | cut slides 9–11 (params) first — keep Q/K/V + pattern + ΔE |
| Running late | merge Exercice into Q&A; the sizing table survives on one slide |

## 8. Sources consulted (2026-09-29)

- 3Blue1Brown — *Attention in transformers, step-by-step* (Deep Learning ch. 6) — concepts + 24 figures: https://www.3blue1brown.com/lessons/attention
- llama.cpp README (quick start, backends, quantization, tools): https://github.com/ggml-org/llama.cpp ; server: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- DeepSeek Harness README (npx, plugin architecture, developer preview): https://github.com/deepseek-ai/deepseek-harness
- dsh providers guide (custom API, compat switches, troubleshooting): https://deepseek-harness.github.io/deepseek-harness/en/guide/providers
- Hands-on dsh + Ollama/vLLM/llama.cpp lab (Aug 2026; flags, traps, numbers): https://computingforgeeks.com/deepseek-harness-local-model/
- Agent harness concept (agent = model + harness; ReAct/Toolformer; inner/outer; guides vs sensors): https://en.wikipedia.org/wiki/Agent_harness + Böckeler https://martinfowler.com/articles/harness-engineering.html
- llama.cpp quantization benchmark (Q4_K_M default): https://markaicode.com/benchmarks/llamacpp-inference-benchmark/ ; VRAM guide: https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms
- Model landscape Sept 2026: https://medium.com/@mksl/what-can-a-local-model-do-for-you-early-sept-2026-edition-ba9dadf05d74 ; https://pinggy.io/blog/top_5_local_llm_tools_and_models/ ; https://www.kdnuggets.com/top-7-coding-models-you-can-run-locally-in-2026
- Runner comparison: https://machinelearningmastery.com/ollama-vs-lm-studio-vs-llama-cpp-which-local-ai-runtime-should-you-use-in-2026/ ; https://inventivehq.com/blog/ollama-vs-lm-studio-vs-llama-cpp

## 9. Verify-before-teaching checklist (day before)

1. `llama --version` / releases page → build tag used in slides.
2. Qwen3.5-0.8B-GGUF repo still exists on HF (demo command copy-pastes from llama.cpp README).
3. dsh: `npx @deepseek-ai/dsh web` still the launch command; config path (`cordis.patch.yml` vs `settings.yaml`) matches installed version (dsh is **developer preview**).
4. `--jinja` still the tool-calling switch; Ollama/vLLM numbers if quoted.
5. 3b1b figures: license/attribution OK for a non-commercial club session (deck is CC BY-NC-SA; see [img/README.md](./img/README.md)).
6. Node ≥ 22.19/24 on demo machine for dsh.

## 10. Repo contents

```
formationLLM/
├── plan.md                      ← this plan
├── flake.nix / flake.lock       ← nix develop → texliveFull+make; nix build → PDF reproducible
├── formation_llm.tex            ← Beamer deck (French), 38 frames (incl. 2 slides d'installation dsh sur Debian), template-faithful
├── formation_llm.pdf            ← compiled (38 pages, 5.2 MB)
├── Makefile                     ← latexmk build (mirrors Git repo Makefile)
├── img/                         ← 24 3b1b figures + logo.png + README (attribution/licence)
└── demo/
    ├── demo_llama.sh            ← Demo A + B launcher
    └── dsh-provider-example.yaml← dsh local-provider config sample
```

**Status (2026-09-29)**: deck compiles clean — `nix develop` then `make` (flake provides texliveFull + gnumake + git + poppler-utils; `nix build` produces the identical PDF reproducibly) → exit 0, no overfull/underfull boxes (38 pages); layout visually verified on rendered pages (images, tikz diagrams, tables all fit). Note: `flake.nix`/`flake.lock` are **not** tracked by the outer git repo, so `nix develop`/`nix build` fail with "not tracked by Git" until committed (or use the `path:` flake workaround). Still to do before teaching: the §9 verify checklist (T-7) and a live dry-run of Demo A + B on the venue machine.
