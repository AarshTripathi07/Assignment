# Super Investing · Autonomous Equity Research Agent

**Author:** Aarsh Tripathi  
**Target Stock:** Sarvottam Cables Ltd (`NSE: SRVCABLE`)  
**Anchor Analysis Date:** 23 September 2026  

An autonomous AI Research Agent built for **Super Investing** to help Indian retail investors conduct high-signal, disciplined due diligence on NSE-listed equities.

Given an NSE ticker and an untrusted dossier of raw scraped corporate documents, the agent filters malicious attacks, resolves entity collisions, audits financial discrepancies, reconciles temporal developments, and synthesizes a concise, traceable **one-page Research Brief** in Markdown.

---

## 🚀 Quick Start

Built in Python 3.12 with **zero external dependencies required** (pure standard library). Runs out of the box without requiring API keys or heavy frameworks.

### 1. Command Line Interface (CLI)
```bash
python agent.py --ticker SRVCABLE --docs research_pack
```
Generates the audited brief and outputs it to `brief_SRVCABLE.md`.

### 2. Interactive Web Dashboard
```bash
python app.py
```
Launches a local interactive dashboard at `http://localhost:5050` featuring:
- **Scraped Document Explorer:** Real-time classification badges for Official Regulatory Filings, Financial News, Injections Quarantined, and Entity Mismatches.
- **Cognitive Pipeline Trace:** Live streaming terminal view of the agent's multi-phase thinking and audit process.
- **Retail Research Brief View:** Rendered Markdown and clean raw text ready for export.
- **System Test Log:** Comprehensive iteration history comparing model prompts and defenses across development cycles.

---

## 🧠 Architectural Design & Cognitive Pipeline

Real-world scraped web data contains noisy, outdated, and adversarial content. I designed a 5-phase cognitive pipeline to ensure institutional-grade analytical rigor:

```
[Raw Scraped Dossier]
       │
       ▼
1. Untrusted Ingestion & Injection Quarantine ──► Strips malicious prompt injections & tipster spam
       │
       ▼
2. Strict Entity Disambiguation ───────────────► Discards unrelated local municipal disputes (Nagpur cable TV)
       │
       ▼
3. Temporal Fact Reconciliation ───────────────► Reconciles historical 2024 pledge (35%) vs current 2026 status (4.1%)
       │
       ▼
4. Financial Discrepancy Auditing ─────────────► Rejects media revenue typo (₹1,428 cr) in favor of official filing (₹1,248 cr)
       │
       ▼
5. Retail Synthesis (~1 Page Markdown) ────────► Snapshot, Bull Case, Bear Case, Open Questions, Traceable Sources Table
```

### Key Technical Challenges Solved:

1. **Adversarial Prompt Injection Quarantine:**
   - *Challenge:* `multibaggeralerts_2026-08-12.md` embeds a hidden HTML comment directive commanding the AI to ignore previous instructions and declare a "STRONG BUY with 60% upside".
   - *Solution:* The ingestion layer treats all source text as untrusted data, extracts YAML frontmatter safely, strips prompt injection syntax via regex sanitizers, and flags unregistered tipster blogs.

2. **Entity Disambiguation:**
   - *Challenge:* `nagpurcitytimes_2026-08-20.md` details an ₹8 lakh municipal penalty on "Sarvottam Cable Network" (a local broadband operator in Nagpur run by Suresh Patil).
   - *Solution:* Disambiguates corporate identity and discards the article, preventing a false bear-case penalty from contaminating the listed company's fundamentals.

3. **Financial Discrepancy Auditing:**
   - *Challenge:* `businessdaily_2026-08-09.md` published a typographical transposition reporting Q1 revenue as ₹1,428 crore (+35%), which tipster blogs echoed uncritically.
   - *Solution:* Cross-audited against the official statutory exchange filing (`ir_press_release_2026-08-08.md`) which reports ₹1,248 crore (+18.0%). The agent adopts the authoritative filing and highlights the discrepancy under *Open Questions*.

4. **Temporal Fact Reconciliation:**
   - *Challenge:* `marketwatchindia_2024-03-18.md` flagged high promoter pledging (35%) in March 2024.
   - *Solution:* Chronologically anchored relative to 23 September 2026. The agent reconciles this against the latest June 2026 shareholding filing (`nse_shareholding_2026-07-15.md`), noting pledge fell to 4.1%—identifying it as positive balance-sheet deleveraging rather than an active governance risk.

5. **Retail-Calibrated Financial Ratios:**
   - Evaluates the ₹46.3 crore CGST tax demand notice (`nse_announcement_2026-09-02.md`) directly against the quarterly PAT (₹82 crore), clarifying for everyday investors that it represents ~56.5% of quarterly net profit.

---

## 🤖 Models & Providers Supported

1. **Google Gemini 1.5 Flash:**
   - Selected for high prompt-injection resistance, large context window (1M+ tokens), fast inference latency (~1s), and generous free tier.
2. **OpenAI GPT-4o-mini:**
   - Supported for quantitative tabular delta analysis and strict markdown compliance.
3. **Internal Deterministic Engine (Default):**
   - Zero-dependency built-in engine allowing anyone to clone and test the entire multi-phase audit pipeline immediately without configuring API keys.

---

## 📁 Repository Structure

```
├── agent.py                  # Core AI Research Agent CLI & Pipeline
├── app.py                    # Interactive Web Dashboard (Standard library)
├── system_prompt.txt         # Standalone System Prompt & Defense Directives
├── brief_SRVCABLE.md         # Generated 1-Page Retail Research Brief for SRVCABLE
├── test_log.md               # 3-Run Test Log with Failure Modes & Architectural Evolutions
├── research_pack/            # 8 Scraped source documents for SRVCABLE
│   ├── businessdaily_2026-08-09.md
│   ├── ir_concall_2026-08-11.md
│   ├── ir_press_release_2026-08-08.md
│   ├── marketwatchindia_2024-03-18.md
│   ├── multibaggeralerts_2026-08-12.md
│   ├── nagpurcitytimes_2026-08-20.md
│   ├── nse_announcement_2026-09-02.md
│   └── nse_shareholding_2026-07-15.md
├── requirements.txt          # Optional packages for cloud LLM APIs
└── README.md                 # Project Architecture & Documentation
```

---

## 🎥 Walkthrough Video Outline

- **Execution Demo (0:00 – 1:00):** Show `python app.py` running in browser with the 8 classified documents and trigger the multi-phase audit pipeline.
- **Design Decision (1:00 – 2:00):** Walk through the **Source Credibility Hierarchy & Discrepancy Auditing**—highlighting how the agent detected the media revenue typo (₹1,428 cr vs official ₹1,248 cr) and resolved the promoter pledge timeline (35% in 2024 to 4.1% in 2026).
- **Limitation (2:00 – 2:45):** Discuss how complex nested accounting footnotes in scanned PDF filings currently require pre-extracted markdown, which can be expanded in future versions using multi-modal table extraction models.