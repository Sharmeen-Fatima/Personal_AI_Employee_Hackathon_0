"""
Gold Tier — LIVE Demo (Real Credentials)
==========================================
Credentials .env file se load hoti hain.
WhatsApp: Twilio API se messages fetch + send karta hai.
Odoo ERP: XML-RPC se real records create/fetch karta hai.

Usage:
    python run_gold_live.py
"""

import sys
import os

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env credentials
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

TWILIO_SID         = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_TOKEN       = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_WA_NUMBER   = os.environ.get("TWILIO_WHATSAPP_NUMBER", "").strip()
YOUR_WA_NUMBER     = os.environ.get("YOUR_WHATSAPP_NUMBER", "").strip()

ODOO_URL           = os.environ.get("ODOO_URL", "http://localhost:8069").strip()
ODOO_DB            = os.environ.get("ODOO_DB", "odoo").strip()
ODOO_USERNAME      = os.environ.get("ODOO_USERNAME", "admin").strip()
ODOO_PASSWORD      = os.environ.get("ODOO_PASSWORD", "admin").strip()

VAULT              = os.path.join(os.path.dirname(os.path.abspath(__file__)), "obsidian-vault")

print("=" * 60)
print("  GOLD TIER — Live Demo (Real Credentials)")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# Credential check
# ─────────────────────────────────────────────────────────────
print("\n🔑 Credential Check")
print("-" * 40)
print(f"   Twilio SID      : {TWILIO_SID[:8]}...{'✅' if TWILIO_SID else '❌'}")
print(f"   Twilio Token    : {'✅ set' if TWILIO_TOKEN else '❌ NOT SET'}")
print(f"   Twilio WA No.   : {TWILIO_WA_NUMBER or '❌ NOT SET'}")
print(f"   Your WA Number  : {YOUR_WA_NUMBER or '❌ NOT SET'}")
print(f"   Odoo URL        : {ODOO_URL}")
print(f"   Odoo DB         : {ODOO_DB}")
print(f"   Odoo Username   : {ODOO_USERNAME}")
print(f"   Odoo Password   : {'✅ set' if ODOO_PASSWORD else '❌ NOT SET'}")

missing = []
if not TWILIO_SID:    missing.append("TWILIO_ACCOUNT_SID")
if not TWILIO_TOKEN:  missing.append("TWILIO_AUTH_TOKEN")
if not TWILIO_WA_NUMBER: missing.append("TWILIO_WHATSAPP_NUMBER")

if missing:
    print(f"\n❌ Missing credentials: {', '.join(missing)}")
    print("   .env file mein yeh values fill karo phir dobara run karo.")
    sys.exit(1)

print("\n✅ All required credentials loaded.")


# ─────────────────────────────────────────────────────────────
# STEP 1: WhatsApp — Twilio Health Check + Fetch Messages
# ─────────────────────────────────────────────────────────────
print("\n\n💬 STEP 1: WhatsApp — Twilio Live Connection")
print("-" * 40)

from golden_tier_external_world.watchers.whatsapp.client import RealWhatsAppClient
from golden_tier_external_world.watchers.whatsapp.models import WhatsAppConfig
from golden_tier_external_world.watchers.whatsapp.watcher import WhatsAppWatcher

wa_config = WhatsAppConfig(
    phone_number=TWILIO_WA_NUMBER,
    vault_root=VAULT,
    max_results=10,
    poll_interval_secs=30.0,
    send_read_receipts=False,
)
wa_client = RealWhatsAppClient(
    wa_config,
    account_sid=TWILIO_SID,
    credential_token=TWILIO_TOKEN,
)

print("🔍 WhatsApp health check (Twilio API)...")
wa_healthy = wa_client.health_check()
print(f"   Status: {'✅ Connected' if wa_healthy else '❌ Failed (check Twilio credentials)'}")

wa_messages_found = 0
if wa_healthy:
    print("\n📬 Fetching recent inbound WhatsApp messages (up to 10)...")
    wa_messages = wa_client.fetch_messages(max_results=10)
    wa_messages_found = len(wa_messages)
    print(f"   Inbound messages found: {wa_messages_found}")

    if wa_messages:
        print("\n   Recent messages:")
        for i, msg in enumerate(wa_messages[:5], 1):
            print(f"   {i}. From: {msg.sender_phone}")
            print(f"      Body: {msg.message_body[:60] or '(media/empty)'}")
            if msg.received_at:
                print(f"      At: {msg.received_at.strftime('%Y-%m-%d %H:%M UTC')}")
    else:
        print("   (No inbound messages yet — send a WhatsApp message to the sandbox number first)")
        print(f"   Sandbox number: {TWILIO_WA_NUMBER}")

    # Run WhatsAppWatcher tick
    print("\n⏱  Running WhatsAppWatcher tick...")
    wa_watcher = WhatsAppWatcher(wa_config, client=wa_client)
    wa_watcher.start()
    wa_tick = wa_watcher.tick()
    print(f"   Health: {'OK' if wa_tick.health_ok else 'FAIL'}")
    print(f"   Events found: {wa_tick.events_found}")
    print(f"   Errors: {wa_tick.errors}")

else:
    print("\n   ⚠️  WhatsApp skipped (Twilio connection failed).")
    print("   Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env")


# ─────────────────────────────────────────────────────────────
# STEP 2: WhatsApp — Send Test Message
# ─────────────────────────────────────────────────────────────
print("\n\n📤 STEP 2: WhatsApp — Send Test Message")
print("-" * 40)

wa_sent_ok = False

if not wa_healthy:
    print("   ⚠️  Skipped (Twilio not connected).")
elif not YOUR_WA_NUMBER:
    print("   ⚠️  YOUR_WHATSAPP_NUMBER not set in .env — skipping send test.")
    print("   Add: YOUR_WHATSAPP_NUMBER=+923xxxxxxxxx in .env")
else:
    test_message = (
        "🤖 Gold Tier AI Agent Test Message\n"
        "Ye message automatically bheja gaya hai GIAIC Hackathon ke Gold Tier demo se.\n"
        "WhatsApp + Twilio integration LIVE chal rahi hai!\n"
        "- Personal AI Employee System"
    )

    print(f"   To: {YOUR_WA_NUMBER}")
    print(f"   From: {TWILIO_WA_NUMBER}")
    print(f"   Message: {test_message[:80]}...")
    print("\n👤 Simulating HITL approval for WhatsApp send...")
    print("   ✅ Approved!")

    print("\n🚀 Sending WhatsApp message via Twilio...")
    wa_sent_ok = wa_client.send_message(YOUR_WA_NUMBER, test_message)
    if wa_sent_ok:
        print(f"   ✅ WhatsApp message sent to {YOUR_WA_NUMBER}!")
        print(f"   📱 Check your WhatsApp — message should arrive shortly.")
    else:
        print(f"   ❌ Send failed.")
        print(f"   ⚠️  Make sure you have joined the Twilio sandbox first:")
        print(f"       Send 'join <your-sandbox-code>' to {TWILIO_WA_NUMBER} on WhatsApp")


# ─────────────────────────────────────────────────────────────
# STEP 3: Odoo ERP — Health Check + Create + Fetch Record
# ─────────────────────────────────────────────────────────────
print("\n\n🏢 STEP 3: Odoo ERP — XML-RPC Live Connection")
print("-" * 40)

from golden_tier_external_world.actions.odoo.adapter import RealOdooAdapter
from golden_tier_external_world.actions.odoo.models import (
    OdooConfig, OdooActionStatus,
    make_create_request, make_fetch_request, make_update_request,
)

odoo_config = OdooConfig(
    vault_root=VAULT,
    odoo_url=ODOO_URL,
    database=ODOO_DB,
)
odoo_adapter = RealOdooAdapter(
    odoo_config,
    username=ODOO_USERNAME,
    credential_token=ODOO_PASSWORD,
)

print(f"🔍 Odoo health check ({ODOO_URL})...")
odoo_healthy = odoo_adapter.health_check()
print(f"   Status: {'✅ Connected' if odoo_healthy else '❌ Failed (check Docker + Odoo URL/DB/credentials)'}")

odoo_record_id = None

if odoo_healthy:
    # --- Create a Contact (res.partner) ---
    print("\n📝 Creating a new Contact in Odoo (res.partner)...")
    print("👤 Simulating HITL approval for Odoo record creation...")
    print("   ✅ Approved!")

    create_req = make_create_request(
        model="res.partner",
        data={
            "name": "GIAIC Hackathon AI Agent",
            "email": "ai.agent@hackathon.giaic",
            "phone": "+923162233896",
            "comment": "Created by Gold Tier AI Agent — GIAIC Hackathon 2026",
        },
        tier=1,  # tier=1 for demo (no HITL blocking)
    )

    create_result = odoo_adapter.execute(create_req)
    if create_result.status == OdooActionStatus.SUCCESS:
        odoo_record_id = create_result.record_id
        print(f"   ✅ Contact created!")
        print(f"   Record ID: {odoo_record_id}")
        print(f"   Name: {create_result.record_data.get('name', 'N/A')}")
        print(f"   Email: {create_result.record_data.get('email', 'N/A')}")
    else:
        print(f"   ❌ Create failed: {create_result.error}")

    # --- Fetch the created record ---
    if odoo_record_id:
        print(f"\n🔍 Fetching record ID {odoo_record_id} from Odoo...")
        fetch_req = make_fetch_request(
            model="res.partner",
            record_id=odoo_record_id,
            tier=1,
        )
        fetch_result = odoo_adapter.execute(fetch_req)
        if fetch_result.status == OdooActionStatus.SUCCESS:
            print(f"   ✅ Record fetched successfully!")
            data = fetch_result.record_data
            print(f"   Name  : {data.get('name', 'N/A')}")
            print(f"   Email : {data.get('email', 'N/A')}")
            print(f"   Phone : {data.get('phone', 'N/A')}")
        else:
            print(f"   ❌ Fetch failed: {fetch_result.error}")

    # --- Update the record ---
    if odoo_record_id:
        print(f"\n✏️  Updating record ID {odoo_record_id} in Odoo...")
        print("👤 Simulating HITL approval for Odoo record update...")
        print("   ✅ Approved!")

        update_req = make_update_request(
            model="res.partner",
            record_id=odoo_record_id,
            data={"comment": f"Updated by Gold Tier AI Agent — GIAIC Hackathon 2026. Record ID: {odoo_record_id}"},
            tier=1,
        )
        update_result = odoo_adapter.execute(update_req)
        if update_result.status == OdooActionStatus.SUCCESS:
            print(f"   ✅ Record updated successfully!")
        else:
            print(f"   ❌ Update failed: {update_result.error}")

else:
    print("\n   ⚠️  Odoo skipped (connection failed).")
    print("   Docker container chal raha hai? Run:")
    print("   docker run -d --name odoo17 -p 8069:8069 odoo:17")
    print(f"   Then open: {ODOO_URL}")
    print("   Database setup karo: mycompany / admin@mycompany.com / admin123")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n")
print("=" * 60)
print("  GOLD TIER — Live Demo Complete!")
print("=" * 60)
print(f"""
{'✅' if wa_healthy       else '⚠️ '} WhatsApp Watcher   — {'Connected, ' + str(wa_messages_found) + ' messages fetched' if wa_healthy else 'Twilio connection failed (check credentials)'}
{'✅' if wa_sent_ok       else '⚠️ '} WhatsApp Send      — {'Message sent to ' + YOUR_WA_NUMBER if wa_sent_ok else 'Skipped (join sandbox or check YOUR_WHATSAPP_NUMBER)'}
{'✅' if odoo_healthy     else '⚠️ '} Odoo ERP           — {'Connected, record ID ' + str(odoo_record_id) + ' created' if odoo_record_id else ('Connected but no record created' if odoo_healthy else 'Docker not running (start with: docker run odoo:17)')}

📁 Vault logs:
   obsidian-vault/70-LOGS/  ← All watcher + action logs

🔑 Credentials used:
   Twilio WhatsApp : {TWILIO_WA_NUMBER}
   Odoo ERP        : {ODOO_URL} (DB: {ODOO_DB})

🏆 Gold Tier: WhatsApp + Odoo ERP LIVE
""")
