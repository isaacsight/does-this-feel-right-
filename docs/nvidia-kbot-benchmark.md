# NVIDIA Release Intelligence & Local K:BOT Setup Guide

*Saved: July 25, 2026*  
*Hardware Target: Apple M3 Max (36 GB Unified Memory)*

---

## 1. NVIDIA Release Highlights (July 2026)

### GPU Drivers & Software
* **Stable Driver Branch:** `610.74` / `610.82 Beta`.
* **Legacy Arch EOL:** Pascal, Maxwell, and Volta driver support has transitioned to legacy security maintenance (582.x series).

### Datacenter Architecture
* **Blackwell Ultra (B300 Series):** Production rollout with expanded HBM memory footprints and compute density upgrades.
* **Vera Rubin Architecture:** Announced at GTC, next-gen datacenter platform shipping in H2 2026.

### Developer & AI Platforms
* **CUDA Toolkit 13.3.1 / 13.4 Developer Preview:** Dropped legacy support for Volta/Pascal/Maxwell; optimized runtime targets for Turing, Ampere, Ada, Hopper, Blackwell, and Rubin.
* **NVIDIA Cosmos 3 & Cosmos 3 Edge:** Open-weight physical AI world foundation models. `Cosmos 3 Edge` (4B parameters) is tailored for real-time edge robotics and Jetson platforms under the **NVIDIA Open Model License** (permits commercial use).

---

## 2. Apple M3 Max Local Model Benchmark Results

Ran full benchmark comparing local models on **Apple M3 Max (36 GB Unified Memory)** using `ollama_benchmark.py`:

| Model Name | Parameter Size | Speed (Tokens/sec) | Time to First Token | Use Case / Notes |
| :--- | :---: | :---: | :---: | :--- |
| **`nemotron-mini:latest`** | 4.2B | **33.72 tok/s** | **0.899s** | **Ultra-low latency** (Instant CLI routing & micro-agent queries) |
| **`gemma4:latest`** | 8.0B | **36.22 tok/s** | 15.120s | Fast general response generation |
| **`mistral-nemo`** | **12.0B** | **20.33 tok/s** | 39.237s | **NVIDIA & Mistral co-developed, 128k context, FP8 trained** |
| **`qwen3:8b`** | 8.2B | **24.78 tok/s** | 2.751s | Quality prose & quick response |
| **`deepseek-r1:14b`** | 14.8B | **15.63 tok/s** | 4.742s | Reasoning & step-by-step logic |
| **`phi4:14b`** | 14.7B | **14.88 tok/s** | 4.912s | Balanced instruction following |
| **`qwen2.5-coder:32b`** | 32.8B | **5.57 tok/s** | 9.345s | Heavy architectural code generation |
| **`gemma4:31b`** | 31.3B | **6.67 tok/s** | 56.071s | Deep model synthesis |

---

## 3. Local K:BOT Configuration ($0 API Cost)

### Updated Provider Config
`src/engine/providers/ollama.ts` defaults:
* **Fast Tier:** `nemotron-mini:latest` (4.2B)
* **Strong Tier:** `mistral-nemo:latest` (12B)

### K:BOT Terminal Commands
```bash
# Set kbot to use local Nemotron models
kbot config set model ollama/nemotron-mini
# or for complex coding:
kbot config set model ollama/mistral-nemo

# Run local zero-cost prompts
kbot "draft unit tests for src/engine/providers/ollama.ts"

# Serve local tools to kernel.chat UI
kbot serve
```
