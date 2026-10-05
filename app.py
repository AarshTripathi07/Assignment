"""
Super Investing · AI Research Agent Web Dashboard
Zero-dependency interactive Web UI for evaluating research documents, 
auditing adversarial attacks, and viewing retail research briefs.
"""

import os
import sys
import json
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from agent import ResearchAgent, DEFAULT_TICKER, DEFAULT_ANCHOR_DATE

PORT = 5050
ROOT_DIR = Path(__file__).parent


class ResearchDashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_text(self, text, content_type="text/plain; charset=utf-8", status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html_content = get_dashboard_html()
            self._send_text(html_content, content_type="text/html; charset=utf-8")
        elif self.path == "/api/documents":
            agent = ResearchAgent(ticker=DEFAULT_TICKER)
            docs = agent.load_documents()
            payload = []
            for d in docs:
                payload.append({
                    "filename": d.filename,
                    "metadata": d.metadata,
                    "credibility_tier": d.credibility_tier,
                    "has_injection": d.has_injection,
                    "is_entity_match": d.is_entity_match,
                    "entity_mismatch_reason": d.entity_mismatch_reason,
                    "preview": d.raw_text[:350]
                })
            self._send_json({"documents": payload, "ticker": DEFAULT_TICKER, "anchor_date": DEFAULT_ANCHOR_DATE})
        elif self.path == "/api/brief":
            brief_file = ROOT_DIR / "brief_SRVCABLE.md"
            content = brief_file.read_text(encoding="utf-8") if brief_file.exists() else "# No brief generated yet"
            self._send_json({"brief": content})
        elif self.path == "/api/testlog":
            log_file = ROOT_DIR / "test_log.md"
            content = log_file.read_text(encoding="utf-8") if log_file.exists() else "# No test log available"
            self._send_json({"test_log": content})
        elif self.path == "/api/prompt":
            prompt_file = ROOT_DIR / "system_prompt.txt"
            content = prompt_file.read_text(encoding="utf-8") if prompt_file.exists() else ""
            self._send_json({"prompt": content})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/run":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            params = json.loads(body) if body else {}

            ticker = params.get("ticker", DEFAULT_TICKER)
            provider = params.get("provider", "offline")
            api_key = params.get("apiKey", "")
            model = params.get("model", "")

            agent = ResearchAgent(ticker=ticker)
            agent.load_documents()
            brief = agent.generate_brief_llm(provider=provider, api_key=api_key or None, model=model or None)

            # Save the brief to disk
            brief_file = ROOT_DIR / f"brief_{ticker}.md"
            with open(brief_file, "w", encoding="utf-8") as f:
                f.write(brief)

            self._send_json({
                "success": True,
                "brief": brief,
                "audit_log": agent.audit_log,
                "stats": {
                    "total_docs": len(agent.documents),
                    "active_docs": len([d for d in agent.documents if d.is_entity_match]),
                    "injections_quarantined": len([d for d in agent.documents if d.has_injection]),
                    "entity_mismatches": len([d for d in agent.documents if not d.is_entity_match])
                }
            })
        else:
            self.send_error(404, "Not Found")


def get_dashboard_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Super Investing · AI Research Agent Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(18, 24, 38, 0.85);
      --card-border: #1e293b;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --emerald: #10b981;
      --rose: #f43f5e;
      --amber: #f59e0b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      line-height: 1.5;
      padding-bottom: 40px;
    }
    header {
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 16px 32px;
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo-group { display: flex; align-items: center; gap: 12px; }
    .badge {
      background: #1e1b4b;
      color: #818cf8;
      border: 1px solid #3730a3;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
    }
    .container { max-width: 1400px; margin: 24px auto; padding: 0 24px; display: grid; grid-template-columns: 420px 1fr; gap: 24px; }
    @media (max-width: 1024px) { .container { grid-template-columns: 1fr; } }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .card h3 { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: var(--text); display: flex; justify-content: space-between; align-items: center; }
    .btn {
      background: var(--primary);
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .btn:hover { background: var(--primary-hover); transform: translateY(-1px); }
    .btn-secondary {
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
    }
    .btn-secondary:hover { background: #334155; }
    .doc-item {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 12px;
      margin-bottom: 10px;
      font-size: 13px;
      transition: border-color 0.2s;
    }
    .doc-item:hover { border-color: #3b82f6; }
    .doc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
    .doc-title { font-weight: 600; color: #e2e8f0; font-size: 13px; }
    .doc-tag { font-size: 10px; padding: 2px 6px; border-radius: 4px; text-transform: uppercase; font-weight: 700; }
    .tag-tier1 { background: #064e3b; color: #34d399; }
    .tag-tier2 { background: #1e3a8a; color: #60a5fa; }
    .tag-tier3 { background: #881337; color: #fb7185; }
    .tag-warn { background: #78350f; color: #fbbf24; }
    .doc-meta { color: var(--text-muted); font-size: 11px; margin-bottom: 6px; }
    .nav-tabs { display: flex; gap: 8px; border-bottom: 1px solid var(--card-border); margin-bottom: 18px; }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 10px 16px;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-btn.active { color: var(--primary); border-bottom-color: var(--primary); }
    .brief-render {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 24px;
      color: #e2e8f0;
      line-height: 1.65;
    }
    .brief-render h1 { font-size: 20px; color: #fff; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 8px; }
    .brief-render h2 { font-size: 16px; color: #818cf8; margin-top: 18px; margin-bottom: 8px; }
    .brief-render p, .brief-render ul { margin-bottom: 12px; font-size: 14px; }
    .brief-render ul { padding-left: 20px; }
    .brief-render li { margin-bottom: 6px; }
    .brief-render table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 12px; }
    .brief-render th, .brief-render td { border: 1px solid #334155; padding: 8px; text-align: left; }
    .brief-render th { background: #1e293b; color: #94a3b8; font-weight: 600; }
    .brief-render code { background: #1e293b; color: #f43f5e; padding: 2px 5px; border-radius: 4px; font-size: 12px; }
    .log-terminal {
      background: #000;
      color: #10b981;
      font-family: "Cascadia Code", Consolas, monospace;
      padding: 14px;
      border-radius: 8px;
      font-size: 12px;
      height: 380px;
      overflow-y: auto;
      border: 1px solid #22c55e33;
    }
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #10b981;
      background: #064e3b33;
      padding: 4px 10px;
      border-radius: 9999px;
      border: 1px solid #064e3b;
    }
    .pulse-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
    .raw-textarea {
      width: 100%;
      height: 520px;
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 8px;
      color: #94a3b8;
      font-family: monospace;
      font-size: 13px;
      padding: 16px;
      resize: vertical;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo-group">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
      </svg>
      <div>
        <h1 style="font-size: 18px; font-weight: 700;">Super Investing · AI Research Agent</h1>
        <div style="font-size: 11px; color: var(--text-muted);">Long-term Indian Equities Due Diligence Engine</div>
      </div>
      <span class="badge">NSE: SRVCABLE</span>
      <span class="badge" style="background:#042f2e; color:#2dd4bf; border-color:#0d9488;">Anchor: 23-Sep-2026</span>
    </div>
    <div style="display:flex; gap:12px; align-items:center;">
      <div class="status-pill"><span class="pulse-dot"></span> Agent Ready</div>
      <button class="btn" id="runBtn" onclick="runAgentAnalysis()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        Run Agent Analysis
      </button>
    </div>
  </header>

  <div class="container">
    <!-- LEFT COLUMN: Scraped Documents Explorer -->
    <div class="card">
      <h3>
        <span>Scraped Research Pack</span>
        <span id="docCount" style="font-size: 12px; color: var(--text-muted);">8 Documents</span>
      </h3>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 14px;">
        Simulated raw scraped dossier. Each file includes source metadata, publication dates, and untrusted raw text.
      </p>
      <div id="docsList" style="max-height: 640px; overflow-y: auto; padding-right: 4px;">
        <div style="color: var(--text-muted); font-size: 12px;">Loading documents...</div>
      </div>
    </div>

    <!-- RIGHT COLUMN: Agent Execution, Brief & Audit Logs -->
    <div class="card">
      <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('briefTab', this)">Generated Research Brief</button>
        <button class="tab-btn" onclick="switchTab('auditTab', this)">Agent Reasoning Log</button>
        <button class="tab-btn" onclick="switchTab('rawTab', this)">Raw Markdown View</button>
        <button class="tab-btn" onclick="switchTab('testlogTab', this)">System Test Log</button>
      </div>

      <!-- Tab 1: Rendered Brief -->
      <div id="briefTab">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <span style="font-size: 12px; color: var(--text-muted);">Audited retail research brief · ~1 page format</span>
          <button class="btn btn-secondary" onclick="copyBriefText()" style="font-size: 12px; padding: 6px 12px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Copy Markdown
          </button>
        </div>
        <div id="briefContent" class="brief-render">Loading research brief...</div>
      </div>

      <!-- Tab 2: Agent Reasoning Log -->
      <div id="auditTab" style="display:none;">
        <h4 style="font-size: 14px; margin-bottom: 8px; color: #a5b4fc;">Live Agent Cognitive Pipeline & Audit Trace</h4>
        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">
          Autonomous reasoning trace: Untrusted prompt injection quarantine, entity resolution disambiguation, and financial cross-auditing.
        </p>
        <div id="auditLog" class="log-terminal">Run analysis to stream agent thinking trace...</div>
      </div>

      <!-- Tab 3: Raw Markdown -->
      <div id="rawTab" style="display:none;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <span style="font-size: 12px; color: var(--text-muted);">Clean Markdown source ready for export or report distribution</span>
          <button class="btn btn-secondary" onclick="copyRawText()" style="font-size: 12px; padding: 6px 12px;">Copy Markdown</button>
        </div>
        <textarea id="rawBrief" class="raw-textarea" readonly></textarea>
      </div>

      <!-- Tab 4: Test Log & Iteration History -->
      <div id="testlogTab" style="display:none;">
        <div id="testLogContent" class="brief-render" style="max-height: 600px; overflow-y: auto;">Loading test log...</div>
      </div>
    </div>
  </div>

  <script>
    let currentBriefMarkdown = "";

    async function loadInitialData() {
      // 1. Load documents
      try {
        const resp = await fetch("/api/documents");
        const data = await resp.json();
        renderDocuments(data.documents);
      } catch (err) {
        console.error("Failed to load documents", err);
      }

      // 2. Load current brief
      try {
        const resp = await fetch("/api/brief");
        const data = await resp.json();
        currentBriefMarkdown = data.brief;
        document.getElementById("briefContent").innerHTML = marked.parse(data.brief);
        document.getElementById("rawBrief").value = data.brief;
      } catch (err) {
        console.error("Failed to load brief", err);
      }

      // 3. Load test log
      try {
        const resp = await fetch("/api/testlog");
        const data = await resp.json();
        document.getElementById("testLogContent").innerHTML = marked.parse(data.test_log);
      } catch (err) {
        console.error("Failed to load test log", err);
      }
    }

    function renderDocuments(docs) {
      const container = document.getElementById("docsList");
      document.getElementById("docCount").innerText = `${docs.length} Documents`;
      container.innerHTML = "";

      docs.forEach(doc => {
        const el = document.createElement("div");
        el.className = "doc-item";

        let tagClass = "tag-tier2";
        let tagLabel = "Tier 2: News";
        if (doc.credibility_tier.includes("Tier 1")) { tagClass = "tag-tier1"; tagLabel = "Tier 1: Official"; }
        if (doc.credibility_tier.includes("Tier 3")) { tagClass = "tag-tier3"; tagLabel = "Tier 3: Blog/Spam"; }

        let alertBadge = "";
        if (doc.has_injection) {
          alertBadge = `<span class="doc-tag tag-warn" style="margin-left:4px;">🚨 Injection Quarantined</span>`;
        }
        if (!doc.is_entity_match) {
          alertBadge = `<span class="doc-tag tag-tier3" style="margin-left:4px;">❌ Entity Mismatch (Filtered)</span>`;
        }

        const dateStr = doc.metadata.published || "Unknown Date";
        const sourceStr = doc.metadata.source || doc.filename;

        el.innerHTML = `
          <div class="doc-header">
            <span class="doc-title">${doc.filename}</span>
            <div><span class="doc-tag ${tagClass}">${tagLabel}</span>${alertBadge}</div>
          </div>
          <div class="doc-meta">${dateStr} · ${sourceStr}</div>
          <div style="font-size: 11px; color: #64748b; font-family: monospace; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${doc.preview.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
          </div>
        `;
        container.appendChild(el);
      });
    }

    function switchTab(tabId, btn) {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      ["briefTab", "auditTab", "rawTab", "testlogTab"].forEach(id => {
        document.getElementById(id).style.display = (id === tabId) ? "block" : "none";
      });
    }

    async function runAgentAnalysis() {
      const btn = document.getElementById("runBtn");
      btn.innerHTML = `<span class="pulse-dot"></span> Analyzing Dossier...`;
      btn.disabled = true;

      // Switch to reasoning log tab to show live activity
      const auditBtn = document.querySelectorAll(".tab-btn")[1];
      switchTab("auditTab", auditBtn);
      const logContainer = document.getElementById("auditLog");
      logContainer.innerHTML = "[AGENT INITIATED] Loading documents & starting multi-phase audit...";

      try {
        const resp = await fetch("/api/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ticker: "SRVCABLE", provider: "offline" })
        });
        const result = await resp.json();

        // Animate log output
        logContainer.innerHTML = "";
        result.audit_log.forEach((line, idx) => {
          setTimeout(() => {
            const p = document.createElement("div");
            p.innerText = line;
            if (line.includes("ALERT") || line.includes("Discarded")) p.style.color = "#fbbf24";
            if (line.includes("FINDING")) p.style.color = "#38bdf8";
            logContainer.appendChild(p);
            logContainer.scrollTop = logContainer.scrollHeight;
          }, idx * 60);
        });

        currentBriefMarkdown = result.brief;
        document.getElementById("briefContent").innerHTML = marked.parse(result.brief);
        document.getElementById("rawBrief").value = result.brief;

        setTimeout(() => {
          btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Analysis Complete!`;
          setTimeout(() => {
            btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Re-Run Analysis`;
            btn.disabled = false;
          }, 2000);
        }, result.audit_log.length * 60 + 500);

      } catch (err) {
        logContainer.innerHTML += `\\n[ERROR] Analysis failed: ${err.message}`;
        btn.innerHTML = `Run Agent Analysis`;
        btn.disabled = false;
      }
    }

    function copyBriefText() {
      navigator.clipboard.writeText(currentBriefMarkdown).then(() => {
        alert("Markdown Brief copied to clipboard!");
      });
    }

    function copyRawText() {
      const textarea = document.getElementById("rawBrief");
      textarea.select();
      document.execCommand("copy");
      alert("Raw Markdown copied to clipboard!");
    }

    window.onload = loadInitialData;
  </script>
</body>
</html>"""


def start_server():
    server = HTTPServer(("localhost", PORT), ResearchDashboardHandler)
    url = f"http://localhost:{PORT}"
    print("=" * 70)
    print(f" SUPER INVESTING · AI RESEARCH AGENT WEB DASHBOARD")
    print(f" Web Server running at: {url}")
    print(f" Open your browser to view the interactive dashboard & audit trail.")
    print(" Press Ctrl+C in terminal to stop.")
    print("=" * 70)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard server...")
        server.server_close()


if __name__ == "__main__":
    start_server()
