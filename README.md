# Personal AI Employee — GIAIC Hackathon 0

**Status**: Gold Tier — LIVE with Real Credentials
**Version**: 3.0.0
**Tier**: Gold ✅
**Author**: Sharmeen Fatima

---

## 🎯 Project Overview

A local-first, autonomous **Personal AI Employee** system that monitors Gmail, LinkedIn, WhatsApp, manages Odoo ERP, and posts on Facebook, Instagram & Twitter — all with Human-in-the-Loop approval for every critical action.

Built for GIAIC Hackathon using:
- **Claude AI** as reasoning engine
- **Playwright** for Facebook & Instagram automation (crash-free)
- **Selenium** for LinkedIn & Twitter automation
- **Twilio WhatsApp API** for real WhatsApp monitoring
- **Odoo XML-RPC** for ERP invoice management
- **Gmail SMTP/IMAP** for real email integration
- **Obsidian Vault** as local-first knowledge store
- **Human-in-the-Loop (HITL)** approval system (Tier 0–4)

---

## 🏆 Tier Progress

| Tier | Status | Description |
|------|--------|-------------|
| 🥉 Bronze | ✅ Complete | Core skills, HITL, vault, watchers |
| 🥈 Silver | ✅ Complete | LinkedIn + Gmail LIVE |
| 🥇 Gold | ✅ Complete | WhatsApp + Odoo + Facebook + Instagram + Twitter LIVE |

---

## ⚡ Gold Tier — What Works LIVE

### ✅ WhatsApp Watcher (Twilio)
- Receives WhatsApp messages via Twilio webhook
- Parses message content, sender, media
- Runs HITL approval before any response
- Saves to Obsidian vault for audit trail

### ✅ Odoo ERP Integration
- Connects to Odoo via XML-RPC (Docker or live instance)
- Fetches invoices, creates records, updates statuses
- Full HITL approval before any ERP write operation

### ✅ Facebook Auto-Post (Playwright)
- Persistent browser session (login once, auto-login forever)
- Opens Facebook feed → finds "What's on your mind?" box
- Types post content → clicks Post button → LIVE on Facebook
- Handles popups (Review audience, notifications) automatically

### ✅ Instagram Auto-Post (Playwright)
- Persistent browser session (login once, auto-login forever)
- Auto-generates post image via Pillow (no manual image needed)
- Uploads image → adds caption → clicks Share → LIVE on Instagram

### ✅ Twitter/X Auto-Post (Selenium)
- 2-step login (username → password)
- Finds tweet compose box via data-testid
- Types tweet + hashtags → clicks Post → LIVE on X/Twitter

---

## 🥈 Silver Tier — What Works LIVE

### ✅ LinkedIn Auto-Post (HITL Flow)
```
Draft Post → Pending Approval → Human Approves → LIVE Post on LinkedIn
```
- Opens LinkedIn feed via Selenium Chrome
- Types content + hashtags → Published LIVE

### ✅ Gmail Auto-Send (HITL Flow)
```
Draft Email → Human Approves → Gmail SMTP → Delivered to Recipients
```
- Uses Gmail App Password (SMTP TLS)
- Sends to configured recipients automatically

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
│   │   ├── gmail/          # Gmail IMAP watcher
│   │   ├── linkedin/       # LinkedIn Selenium watcher
│   │   └── whatsapp/       # WhatsApp Twilio watcher (LIVE)
│   └── actions/
│       ├── pw_browser.py   # Shared Playwright base skill
│       ├── facebook/       # PlaywrightFacebookPoster (LIVE)
│       ├── instagram/      # PlaywrightInstagramPoster (LIVE)
│       ├── twitter/        # SeleniumTwitterPoster (LIVE)
│       ├── email/          # EmailAction + RealEmailAdapter (SMTP)
│       ├── linkedin/       # LinkedInPoster (HITL → Selenium)
│       └── odoo/           # Odoo ERP XML-RPC action (LIVE)
├── silver_tier_core_autonomy/
│   ├── plan_loop/          # Plan-loop scheduler
│   └── scheduler/          # Task scheduler
├── bronze_tier_governance/
│   └── hitl/               # Human-in-the-Loop approval system
├── obsidian-vault/
│   ├── Pending_Approval/   # Posts awaiting human approval
│   ├── Approved/           # Approved and published content
│   ├── Done/               # Completed tasks
│   ├── Plans/              # AI-generated task plans
│   ├── 70-LOGS/            # All screenshots + logs
│   └── browser-sessions/   # Persistent Playwright sessions (gitignored)
├── history/prompts/        # Prompt History Records (PHRs)
├── run_social_live.py      # 🚀 Facebook + Instagram + Twitter LIVE
├── run_gold_live.py        # 🚀 WhatsApp + Odoo LIVE
├── run_silver_live.py      # 🚀 LinkedIn + Gmail LIVE
└── .env                    # Credentials (gitignored — never commit)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install selenium webdriver-manager python-dotenv playwright pillow
playwright install chromium
```

### 2. Configure Credentials
Create `.env` file (never commit this):
```env
# Gmail
GMAIL_ACCOUNT_EMAIL=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECIPIENTS=friend@gmail.com

# LinkedIn
LINKEDIN_EMAIL=your@gmail.com
LINKEDIN_PASSWORD=yourpassword
LINKEDIN_PROFILE_URL=https://www.linkedin.com/in/your-name/

# Twitter/X
TWITTER_EMAIL=your@gmail.com
TWITTER_PASSWORD=yourpassword
TWITTER_USERNAME=your_handle

# Facebook
FACEBOOK_EMAIL=your@gmail.com
FACEBOOK_PASSWORD=yourpassword

# Instagram
INSTAGRAM_USERNAME=your_handle
INSTAGRAM_PASSWORD=yourpassword

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Odoo
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

### 3. Run Social Media Tier
```bash
python run_social_live.py
```

**What happens:**
```
STEP 1 — Facebook:   Persistent session → Feed → Post LIVE
STEP 2 — Twitter:    Login → Compose → Tweet LIVE
STEP 3 — Instagram:  Persistent session → Create → Upload image → Post LIVE
```

### 4. Run Gold Tier (WhatsApp + Odoo)
```bash
python run_gold_live.py
```

### 5. Run Silver Tier (LinkedIn + Gmail)
```bash
python run_silver_live.py
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

All social media posts run through **Tier 2 HITL** before publishing.

---

## 🛠️ Key Technical Highlights

- **Playwright persistent sessions** — Facebook & Instagram login once, session saved to disk, auto-login on every future run. No passwords re-entered, no 2FA every time.
- **Subprocess isolation** — Each social platform runs in its own Python subprocess so browser crashes don't affect other platforms.
- **Auto-image generation** — Instagram requires an image; Pillow generates a branded post image automatically if none provided.
- **Shadow DOM traversal** — LinkedIn's post editor is inside Shadow DOM; found via JS `createTreeWalker`.
- **React event dispatch** — After typing, dispatches `input`/`change`/`keyup` events to enable Post button (React state update).
- **Fail-safe HITL** — Every action returns structured result dict, never raises exceptions.

---

## 📊 Current Status — Gold Tier Complete

| Component | Status | Notes |
|-----------|--------|-------|
| Gmail IMAP Watcher | ✅ LIVE | Real IMAP |
| Gmail SMTP Sender | ✅ LIVE | Real email delivery |
| LinkedIn Watcher | ✅ LIVE | Selenium Chrome |
| LinkedIn Auto-Post | ✅ LIVE | Shadow DOM posting |
| WhatsApp Watcher | ✅ LIVE | Twilio webhook |
| Odoo ERP | ✅ LIVE | XML-RPC integration |
| Twitter/X Post | ✅ LIVE | Selenium — tweets working |
| Facebook Post | ✅ LIVE | Playwright — persistent session |
| Instagram Post | ✅ LIVE | Playwright — auto image + persistent session |
| HITL System | ✅ Complete | Tiers 0–4 |
| Obsidian Vault | ✅ Complete | Full audit trail |

---

## 📸 Live Evidence

Screenshots auto-saved in `obsidian-vault/70-LOGS/`:
- `facebook_posted.png` — Facebook LIVE post confirmation
- `instagram_posted.png` — Instagram upload in progress
- `twitter_posted.png` — Tweet posted on X/Twitter

---

## 📝 License

Personal project for GIAIC Hackathon 0.

---

**Last Updated**: 2026-03-28
**Tier**: Gold (LIVE with Real Credentials — All Platforms)
**Author**: Sharmeen Fatima — Creative Coderr
