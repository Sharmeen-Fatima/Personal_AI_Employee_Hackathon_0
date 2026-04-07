"""
Platinum Tier — Local Agent
Runs on Local PC. Reads Pending_Approval drafts, gets human approval, sends emails.
"""

import os
import shutil
import smtplib
import logging
import re
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
VAULT    = Path(__file__).parent / "vault"
PENDING  = VAULT / "Pending_Approval" / "email"
DONE     = VAULT / "Done"
DASHBOARD = VAULT / "Dashboard.md"  # written by Local ONLY

DONE.mkdir(parents=True, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [LOCAL] %(levelname)s — %(message)s",
)
log = logging.getLogger("local_agent")


# ── Send email ─────────────────────────────────────────────────────────────────
def send_email(to: str, subject: str, body: str) -> bool:
    """Send email via Gmail SMTP."""
    try:
        gmail_user = os.getenv("GMAIL_ADDRESS")
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

        msg = MIMEMultipart()
        msg["From"]    = gmail_user
        msg["To"]      = to
        msg["Subject"] = f"Re: {subject}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)

        log.info(f"Email sent to {to} | Subject: {subject}")
        return True
    except Exception as e:
        log.error(f"Send failed: {e}")
        return False


# ── Parse draft file ───────────────────────────────────────────────────────────
def parse_draft(path: Path) -> dict:
    """Extract key fields from a Pending_Approval markdown file."""
    text = path.read_text(encoding="utf-8")

    def extract(label):
        match = re.search(rf"\*\*{label}:\*\*\s*(.+)", text)
        return match.group(1).strip() if match else ""

    # Extract proposed reply block
    reply_match = re.search(
        r"## Proposed Reply \(Cloud Agent Draft\)\n(.+?)---",
        text, re.DOTALL
    )
    draft_body = reply_match.group(1).strip() if reply_match else ""

    return {
        "sender":  extract("From"),
        "subject": extract("Subject"),
        "draft":   draft_body,
    }


# ── Update dashboard ───────────────────────────────────────────────────────────
def update_dashboard(entry: str):
    """Append an entry to Dashboard.md — Local writes ONLY."""
    ts = datetime.utcnow().isoformat()
    line = f"- [{ts}] {entry}\n"
    with open(DASHBOARD, "a", encoding="utf-8") as f:
        f.write(line)


# ── Process one draft ──────────────────────────────────────────────────────────
def process_draft(path: Path):
    """Show draft to human, get approval, send if approved."""
    info = parse_draft(path)

    print("\n" + "="*60)
    print(f"📧 NEW DRAFT FOR APPROVAL")
    print(f"   From:    {info['sender']}")
    print(f"   Subject: {info['subject']}")
    print(f"\n--- Draft Reply ---\n{info['draft']}\n---")
    print("="*60)
    print("\n[A] Approve & Send   [E] Edit draft   [R] Reject")

    choice = input("Your choice: ").strip().upper()

    if choice == "A":
        # Extract sender email
        sender_match = re.search(r"<(.+?)>", info["sender"])
        to_email = sender_match.group(1) if sender_match else info["sender"]

        success = send_email(to_email, info["subject"], info["draft"])
        if success:
            done_path = DONE / f"approved_{path.name}"
            shutil.move(str(path), str(done_path))
            update_dashboard(f"APPROVED & SENT — {info['subject'][:50]} → {to_email}")
            print("✅ Sent and logged to Done/")
        else:
            print("❌ Send failed — check logs")

    elif choice == "E":
        print("Enter your edited reply (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        edited = "\n".join(lines[:-1])

        sender_match = re.search(r"<(.+?)>", info["sender"])
        to_email = sender_match.group(1) if sender_match else info["sender"]

        success = send_email(to_email, info["subject"], edited)
        if success:
            done_path = DONE / f"edited_{path.name}"
            shutil.move(str(path), str(done_path))
            update_dashboard(f"EDITED & SENT — {info['subject'][:50]} → {to_email}")
            print("✅ Edited reply sent and logged.")

    elif choice == "R":
        done_path = DONE / f"rejected_{path.name}"
        shutil.move(str(path), str(done_path))
        update_dashboard(f"REJECTED — {info['subject'][:50]}")
        print("❌ Draft rejected and moved to Done/rejected_*")

    else:
        print("Invalid choice — skipping.")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    log.info("Local Agent started — scanning Pending_Approval/email/")

    drafts = sorted(PENDING.glob("*.md"))
    if not drafts:
        print("✅ No pending approvals right now.")
        return

    print(f"\n📋 {len(drafts)} draft(s) waiting for approval.\n")
    for draft_path in drafts:
        process_draft(draft_path)

    print("\n✅ All drafts processed.")
    update_dashboard(f"Local Agent session complete — {len(drafts)} draft(s) reviewed")


if __name__ == "__main__":
    main()
