# Personal AI Employee — GIAIC Hackathon 0

**Status**: Silver Tier — LIVE with Real Credentials
**Version**: 2.0.0
**Tier**: Silver ✅
**Author**: Sharmeen Fatima

---

## 🎯 Project Overview

A local-first, autonomous **Personal AI Employee** system that monitors LinkedIn, sends emails, and posts content automatically — all while keeping humans in the loop for critical decisions.

Built for GIAIC Hackathon using:
- **Claude AI** as reasoning engine
- **Selenium** for LinkedIn browser automation
- **Gmail SMTP/IMAP** for real email integration
- **Obsidian Vault** as local-first knowledge store
- **Human-in-the-Loop (HITL)** approval system (Tier 0–4)
- **Python Watchers** for continuous monitoring

---

## 🏆 Tier Progress

| Tier | Status | Description |
|------|--------|-------------|
| 🥉 Bronze | ✅ Complete | Core skills, HITL, vault, watchers (mock) |
| 🥈 Silver | ✅ Complete | Real credentials — LinkedIn + Gmail LIVE |
| 🥇 Gold | 🔜 Next | Full autonomy, Odoo ERP, WhatsApp |

---

## ⚡ Silver Tier — What Works LIVE

### ✅ LinkedIn Watcher
- Logs in via **Selenium Chrome** (headless or visible)
- Fetches activity from LinkedIn inbox
- Detects new messages and notifications

### ✅ LinkedIn Auto-Post (HITL Flow)
```
Draft Post → Pending Approval → Human Approves → LIVE Post on LinkedIn
```
- Opens LinkedIn feed in browser
- Finds "Start a post" via JS/Shadow DOM
- Types content (355+ chars) + hashtags
- Clicks Post button → Published LIVE

### ✅ Gmail Auto-Send (HITL Flow)
```
Draft Email → Human Approves → Gmail SMTP → Delivered to Recipients
```
- Uses Gmail App Password (SMTP TLS)
- Sends to configured recipients automatically
- Same HITL approval flow as LinkedIn

### ✅ Gmail IMAP Watcher
- Fetches unread emails via IMAP SSL
- Parses subject, sender, attachments
- Runs watcher tick for new event detection

---

## 📁 Project Structure

```
Hackathon_0/
├── golden_tier_external_world/
│   ├── watchers/
│   │   ├── gmail/          # Gmail IMAP watcher + RealGmailClient
│   │   ├── linkedin/       # LinkedIn Selenium watcher + RealLinkedInClient
│   │   └── whatsapp/       # WhatsApp watcher (mock)
│   └── actions/
│       ├── email/          # EmailAction + RealEmailAdapter (SMTP)
│       ├── linkedin/       # LinkedInPoster (HITL → Selenium post)
│       ├── browser/        # Browser MCP action
│       └── odoo/           # Odoo ERP action (stub)
├── silver_tier_core_autonomy/
│   ├── plan_loop/          # Plan-loop scheduler
│   └── scheduler/          # Task scheduler
├── bronze_tier_governance/
│   └── hitl/               # Human-in-the-Loop approval system
├── obsidian-vault/
│   ├── Pending_Approval/   # Posts/emails awaiting human approval
│   ├── Approved/           # Approved and published content
│   ├── Done/               # Completed tasks
│   ├── Plans/              # AI-generated task plans
│   └── 70-LOGS/            # All watcher + action logs
├── history/prompts/        # Prompt History Records (PHRs)
├── tests/                  # Unit + integration tests
├── run_silver_live.py      # 🚀 Main Silver Tier live demo
├── run_silver_demo.py      # Demo mode (mock credentials)
└── .env                    # Credentials (gitignored — never commit)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install selenium webdriver-manager python-dotenv
```

### 2. Configure Credentials
Create `.env` file (never commit this):
```env
GMAIL_ACCOUNT_EMAIL=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
LINKEDIN_EMAIL=your@gmail.com
LINKEDIN_PASSWORD=yourpassword
LINKEDIN_PROFILE_URL=https://www.linkedin.com/in/your-name/
EMAIL_RECIPIENTS=friend@gmail.com,colleague@outlook.com
```

**Gmail App Password setup:**
1. Google Account → Security → 2-Step Verification → ON
2. Security → App Passwords → Mail → Generate
3. Copy 16-digit password to `.env`

**Gmail IMAP setup:**
- Gmail → Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP → Save

### 3. Run Silver Tier Demo
```bash
python run_silver_live.py
```

**What happens:**
```
STEP 1 — Gmail IMAP:     Connect → Fetch unread emails → Watcher tick
STEP 2 — LinkedIn Watch: Login → Fetch activity → Watcher tick
STEP 3 — LinkedIn Post:  Draft → HITL Approve → POST LIVE on LinkedIn
STEP 4 — Gmail Send:     Draft → HITL Approve → Email sent to recipients
```

---

## 🔐 HITL Approval Tiers

| Tier | Risk Level | Approval |
|------|-----------|---------|
| 0 | Read-only | Auto |
| 1 | Low risk | Auto |
| 2 | Medium | Human required |
| 3 | High risk | Human required |
| 4 | Critical | Human + audit |

LinkedIn posts and emails run through **Tier 2 HITL** — human approval simulated in demo, real in production.

---

## 🛠️ Skills Inventory (12 Skills)

### Core
- `FILESYSTEM_AUTOMATION_SKILL` — Vault file operations
- `ORCHESTRATOR_SYSTEM_SKILL` — Multi-skill coordination
- `RALPH_WIGGUM_LOOP_SKILL` — Continuous operation loop

### Watchers
- `BASE_WATCHER_CREATION_SKILL` — Watcher framework
- `GMAIL_WATCHER_SKILL` — Email monitoring (LIVE via IMAP)
- `WHATSAPP_WATCHER_SKILL` — WhatsApp monitoring

### Actions
- `EMAIL_MCP_ACTION_SKILL` — Email sending (LIVE via SMTP)
- `BROWSER_MCP_SKILL` — Web automation (Selenium)
- `ODOO_MCP_INTEGRATION_SKILL` — ERP integration

### Safety
- `HUMAN_IN_THE_LOOP_APPROVAL_SKILL` — HITL workflow
- `SECURITY_AND_CREDENTIAL_MANAGEMENT_SKILL` — Security controls

### Business
- `CEO_WEEKLY_AUDIT_SKILL` — Weekly reporting

---

## 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Constitution | ✅ Complete | v1.0.0 ratified |
| Vault Structure | ✅ Complete | All sections operational |
| HITL System | ✅ Complete | Tiers 0–4 working |
| Gmail IMAP Watcher | ✅ LIVE | Real IMAP connection |
| Gmail SMTP Sender | ✅ LIVE | Real email delivery |
| LinkedIn Watcher | ✅ LIVE | Selenium Chrome |
| LinkedIn Auto-Post | ✅ LIVE | Shadow DOM posting |
| Plan Loop Scheduler | ✅ Complete | Silver Tier scheduler |
| WhatsApp Watcher | 🔜 Gold Tier | Stub ready |
| Odoo ERP | 🔜 Gold Tier | Stub ready |

---

## 🔬 Technical Highlights

- **Shadow DOM traversal** — LinkedIn's post editor is inside Shadow DOM; found via JS `createTreeWalker` + recursive shadow root search
- **React event dispatch** — After typing, dispatches `input`/`change`/`keyup` events to enable Post button (React state update)
- **IMAP + SMTP** — Same Gmail App Password works for both reading (IMAP SSL:993) and sending (SMTP STARTTLS:587)
- **Fail-safe HITL** — Every action goes through approval; failures return structured results, never raise exceptions

---

## 📖 Logs & Vault

```
obsidian-vault/Pending_Approval/   ← Posts/emails awaiting approval
obsidian-vault/Approved/           ← Approved content
obsidian-vault/70-LOGS/            ← All system logs
obsidian-vault/70-LOGS/linkedin_feed_screenshot.png
obsidian-vault/70-LOGS/linkedin_after_click.png
```

---

## 📝 License

Personal project for GIAIC Hackathon 0.

---

**Last Updated**: 2026-03-20
**Tier**: Silver (LIVE with Real Credentials)
**Next Milestone**: Gold Tier — WhatsApp + Odoo + Full Autonomy
