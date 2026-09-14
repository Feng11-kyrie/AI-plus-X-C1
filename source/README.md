# CS146S: The Modern Software Developer — Offline Cache

**Stanford University | Fall 2025**  
Cached on: April 2, 2026  
Original site: https://themodernsoftware.dev/

---

## How to Use This Offline Cache

1. **Open `index.html`** in any web browser — this is the main course page with full navigation (Overview, Syllabus, FAQ).
2. All reading materials that could be downloaded are saved locally and linked from the index page.
3. Use the **Syllabus** tab to navigate by week and access all readings, assignments, and lecture slides.

---

## Directory Structure

```
CS146S_offline/
├── index.html              ← Main course page (start here)
├── README.md               ← This file
│
├── pdfs/                   ← Downloaded PDF documents
│   ├── how-openai-uses-codex.pdf
│   ├── how-anthropic-uses-claude-code.pdf
│   └── ai-assisted-code-review-assessment.pdf
│
├── pages/                  ← Downloaded article web pages (31 pages)
│   ├── prompt-engineering-overview.html
│   ├── prompt-engineering-guide.html
│   ├── mcp-introduction.html
│   ├── mcp-server-authentication.html
│   ├── mcp-food-for-thought.html
│   ├── mcp-registry-preview.html
│   ├── specs-are-the-new-source-code.html
│   ├── how-long-contexts-fail.html
│   ├── devin-coding-agents-101.html
│   ├── writing-effective-tools-for-agents.html
│   ├── claude-code-best-practices.html
│   ├── good-context-good-code.html
│   ├── peeking-under-the-hood-of-claude-code.html  ← placeholder (Medium blocked)
│   ├── warp-vs-claude-code.html
│   ├── how-warp-uses-warp.html
│   ├── sast-vs-dast.html
│   ├── copilot-prompt-injection-rce.html
│   ├── finding-vulnerabilities-claude-codex.html
│   ├── agentic-ai-threats.html
│   ├── owasp-top-ten.html
│   ├── context-rot.html
│   ├── code-reviews-just-do-it.html
│   ├── how-to-review-code-effectively.html
│   ├── ai-code-review-best-practices.html
│   ├── code-review-essentials.html
│   ├── lessons-from-ai-code-reviews.html
│   ├── sre-introduction.html
│   ├── observability-basics.html
│   ├── multi-agent-systems-ai-native.html
│   ├── benefits-agentic-ai-oncall.html
│   └── kubernetes-troubleshooting-ai.html
│
└── site/                   ← Original site assets (HTML, CSS, JS)
    └── themodernsoftware.dev/
        ├── index.html
        ├── assets/
        │   ├── index-CgRb4FxC.js
        │   └── index-LDF6HMRx.css
        └── ...
```

---

## What Requires Internet Access

The following resources require an internet connection as they could not be downloaded automatically:

| Resource | Reason |
|---|---|
| YouTube videos (3 links) | Video files not downloaded by design |
| Google Slides presentations (14 links) | Require Google account |
| Google Drive files (5 links) | Require Google account |
| GitHub repositories/pages | Live code repositories |
| "Peeking Under the Hood of Claude Code" | Medium.com blocks automated access |

---

## Course Summary

**CS146S** is a Stanford course on modern AI-assisted software development. It covers:

- **Week 1:** Introduction to LLMs and prompt engineering
- **Week 2:** Coding agents, tool use, and MCP (Model Context Protocol)
- **Week 3:** AI IDEs, context management, and PRDs for agents
- **Week 4:** Claude Code and agentic coding workflows
- **Week 5:** Warp terminal and AI-native development
- **Week 6:** AI security, prompt injection, and vulnerability detection
- **Week 7:** AI-powered code review
- **Week 8:** Full-stack AI development and deployment
- **Week 9:** SRE, observability, and agentic on-call engineering
- **Week 10:** Future of AI in software engineering

**Instructor:** Mihail Eric  
**TAs:** Febie Lin, Brent Ju  
**Units:** 3  
**Classroom:** 420-041
