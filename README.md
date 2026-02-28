# Personal AI Employee - Hackathon 0 (Bronze Tier)

**Status**: Foundation Phase
**Version**: 1.0.0
**Tier**: Bronze

---

## 🎯 Project Overview

A local-first, autonomous Personal AI Employee system built on:
- **Claude Code** as reasoning engine
- **Obsidian** as local-first knowledge vault
- **Python Watchers** for persistence
- **MCP Servers** for external actions
- **Human-in-the-Loop** approval system
- **Ralph Wiggum Loop** for continuous operation

## 📁 Project Structure

```
Hackathon_0/
├── .claude/
│   └── skills/              # Skill library organized by category
│       ├── core/            # Core system skills
│       ├── watchers/        # Event monitoring skills
│       ├── actions/         # External action skills
│       ├── safety/          # Safety and security skills
│       └── business/        # Business intelligence skills
├── .specify/                # Spec-Driven Development artifacts
├── obsidian-vault/          # Knowledge base and memory
├── src/                     # Source code
├── history/                 # Prompt history and decisions
├── constitution.md          # System governance document
└── README.md                # This file
```

## 🛠️ Skills Inventory

### Core (3 skills)
- `FILESYSTEM_AUTOMATION_SKILL` - Vault file operations
- `ORCHESTRATOR_SYSTEM_SKILL` - Multi-skill coordination
- `RALPH_WIGGUM_LOOP_SKILL` - Persistence and continuous operation

### Watchers (3 skills)
- `BASE_WATCHER_CREATION_SKILL` - Watcher framework
- `GMAIL_WATCHER_SKILL` - Email monitoring
- `WHATSAPP_WATCHER_SKILL` - WhatsApp monitoring

### Actions (3 skills)
- `EMAIL_MCP_ACTION_SKILL` - Email sending
- `BROWSER_MCP_SKILL` - Web automation
- `ODOO_MCP_INTEGRATION_SKILL` - ERP integration

### Safety (2 skills)
- `HUMAN_IN_THE_LOOP_APPROVAL_SKILL` - HITL workflow
- `SECURITY_AND_CREDENTIAL_MANAGEMENT_SKILL` - Security controls

### Business (1 skill)
- `CEO_WEEKLY_AUDIT_SKILL` - Weekly reporting

**Total**: 12 skills planned

## 📋 Getting Started

### Prerequisites
- Claude Code CLI installed
- Obsidian installed
- Python 3.9+
- Git

### Setup
1. Read `constitution.md` for system governance
2. Review `obsidian-vault/README.md` for vault structure
3. Check `.claude/skills/` for available skills
4. Follow `QUICK-START.md` in vault for configuration

## 🔐 Governance

This project is governed by `constitution.md` which defines:
- Core operating principles
- HITL approval tiers (0-4)
- Safety boundaries
- Skill design rules
- Evolution path (Bronze → Silver → Gold)

**Key Principle**: Start restrictive, loosen deliberately. Trust is earned.

## 🎓 Bronze Tier Goals

- [ ] Core loop operational (Ralph Wiggum)
- [ ] 3+ skills implemented and tested
- [ ] HITL approval system functional
- [ ] 7 consecutive days uptime
- [ ] 50+ successful HITL approvals
- [ ] Zero security incidents

## 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Constitution | ✅ Complete | v1.0.0 ratified |
| Vault Structure | ✅ Complete | All sections created |
| Skills Structure | ✅ Complete | 12 placeholders created |
| Core Skills | ⏳ Pending | Ready for implementation |
| Watchers | ⏳ Pending | Framework needed |
| Actions | ⏳ Pending | MCP servers needed |
| HITL System | ⏳ Pending | Approval workflow needed |

## 🚀 Next Steps

1. **Implement Core Skills**
   - Start with `FILESYSTEM_AUTOMATION_SKILL`
   - Then `RALPH_WIGGUM_LOOP_SKILL`
   - Finally `ORCHESTRATOR_SYSTEM_SKILL`

2. **Set Up HITL System**
   - Implement `HUMAN_IN_THE_LOOP_APPROVAL_SKILL`
   - Configure approval tiers
   - Test with dummy actions

3. **Build First Watcher**
   - Implement `BASE_WATCHER_CREATION_SKILL`
   - Create framework for other watchers
   - Test with local file watching

4. **Configure MCP Servers**
   - Document in `obsidian-vault/30-INTEGRATIONS/`
   - Set up authentication
   - Test connections

## 📖 Documentation

- **Constitution**: `constitution.md` - System governance
- **Vault Guide**: `obsidian-vault/README.md` - Knowledge base structure
- **Naming Guide**: `obsidian-vault/NAMING-CONVENTIONS.md` - Standards
- **Quick Start**: `obsidian-vault/QUICK-START.md` - 5-minute guide
- **Skill Template**: `.claude/skills/*/SKILL.md` - Placeholder format

## 🔗 Key Links

- [Constitution](./constitution.md) - Governance document
- [Obsidian Vault](./obsidian-vault/) - Knowledge base
- [Skills Directory](./.claude/skills/) - Skill library
- [Prompt History](./history/prompts/) - Decision log

## 📝 License

Personal project - see specific license file if added.

## 🤝 Contributing

This is a personal AI employee project. Contributions follow the governance model defined in `constitution.md`.

---

**Last Updated**: 2026-02-16
**Tier**: Bronze (Foundation)
**Next Milestone**: Core skills implementation
