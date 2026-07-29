# MCP and Skills in Grok Build

Complete [01_Setup.md](01_Setup.md) before starting this file. You also need the warehouse MCP server from [Day 1 - 03_MCP.md](../day1/03_MCP.md).

## Contents

- [1. Same tools, new client](#1-same-tools-new-client)
- [2. Start the warehouse MCP server](#2-start-the-warehouse-mcp-server)
- [3. How Grok finds the MCP server](#3-how-grok-finds-the-mcp-server)
- [4. Transfer the warehouse skill](#4-transfer-the-warehouse-skill)
- [5. Verify with inspect](#5-verify-with-inspect)
- [6. Practical exercise](#6-practical-exercise)
- [7. What you just proved](#7-what-you-just-proved)

## 1. Same tools, new client

On Day 1 you built two portable pieces:

1. An **MCP server** (`inventory_db/inventory_mcp_server.py`) that exposes `query_warehouse_items` and `query_item_details` over HTTP.
2. A **skill** (the warehouse playbook) that tells the model *when* and *how* to use those tools.

You wired both into **Open WebUI**: the MCP URL under Integrations, and the skill body pasted into a system prompt.

Today we move the same pieces into **Grok Build**. We are not rewriting the tools. We are proving the Day 1 claim: MCP and skills travel between clients.

| Piece | Day 1 (Open WebUI) | Day 2 (Grok Build) |
|-------|--------------------|--------------------|
| Tools | MCP at `http://127.0.0.1:8000/mcp` | Same URL, declared in `.grok/config.toml` |
| Skill | Pasted into a custom Model system prompt | `.grok/skills/warehouse-inventory/SKILL.md` |

## 2. Start the warehouse MCP server

Grok does not start this HTTP server for you. Leave it running in a **second terminal** while you work.

Make sure the database exists:

```bash
cd inventory_db
python init_db.py
```

Then start the server:

```bash
python inventory_mcp_server.py
```

You should see Uvicorn listening on `http://127.0.0.1:8000`. Leave that terminal open.

> If `python` isn't found, use `python3`. If port 8000 is busy, stop the other process (often a leftover Day 1 server) and try again.

The MCP endpoint is still:

```text
http://127.0.0.1:8000/mcp
```

That is the same address Open WebUI used on Day 1. One server; two clients.

## 3. How Grok finds the MCP server

Coding agents usually discover MCP from config, not from a GUI form. This repo already ships a **project-scoped** entry:

```toml
# .grok/config.toml
[mcp_servers.warehouse]
url = "http://127.0.0.1:8000/mcp"
enabled = true
```

When you run `grok` from inside `ai-familiarization`, Grok walks up to the repo root, reads `.grok/config.toml`, and connects to that URL.

You can also add servers yourself later:

```bash
grok mcp add warehouse --transport http -- url http://127.0.0.1:8000/mcp
```

Use `--scope project` if you want the CLI to write into `.grok/config.toml` instead of your user config. For this lab the file is already there-no need to re-add it unless yours is missing.

> **Sidebar - stdio vs HTTP:** Many IDE agents prefer **stdio** MCP (they spawn `python inventory_mcp_server.py` and talk over stdin/stdout). Our Day 1 server uses **streamable HTTP** so Open WebUI can reach it. Grok speaks both. Today we reuse HTTP on purpose: zero code changes, clearest transfer story. Stdio is a good follow-on if you want the server to start automatically with the agent.

## 4. Transfer the warehouse skill

On Day 1, Open WebUI had no native skill folders, so you pasted instructions into a system prompt. Grok Build loads skills from disk.

This repo already includes the Day 1 warehouse playbook as a real skill:

```text
.grok/skills/warehouse-inventory/SKILL.md
```

Layout that matters:

1. **Frontmatter** (`name`, `description`) - Grok uses the description to decide *when* the skill is relevant.
2. **Body** - the same rules as Day 1: always call tools for stock questions, never guess quantities, use `item_name`, and so on.

You do not paste this into a system prompt. If the file is under `.grok/skills/` and you launch Grok from the repo, it can load on matching prompts (and may also show up as a slash command like `/warehouse-inventory-assistant`, depending on build).

## 5. Verify with inspect

From the **repo root** (not `inventory_db/`), with `XAI_API_KEY` set and the MCP server still running:

```bash
cd ai-familiarization
grok inspect
```

Confirm you see roughly:

- An MCP server named **warehouse** (or similar), pointed at `http://127.0.0.1:8000/mcp`
- A skill under **warehouse-inventory** / `warehouse-inventory-assistant`

If the MCP looks wrong:

```bash
grok mcp list
grok mcp doctor warehouse
```

`doctor` is the first stop when the server is up but Grok cannot list tools.

## 6. Practical exercise

Stay at the repo root. Use either headless prompts or an interactive `grok` session.

### 6.1 Prove the MCP works

```bash
grok -p "How many hammers are in stock? Use the warehouse tools. Do not edit any files."
```

You should get a real answer from the database (quantity and aisle), not a made-up number. In an interactive session you should see a tool call to `query_item_details`.

Try a list prompt next:

```bash
grok -p "What items do we carry in the warehouse? Use the warehouse tools. Do not edit any files."
```

Expect `query_warehouse_items`, then a list of names from `warehouse.db`.

### 6.2 Prove the skill steers multi-step work

Ask something that needs more than one tool call (the Day 1 loop idea):

```bash
grok -p "Which item do we have the fewest of, and where is it? Use the warehouse tools. Do not edit any files."
```

A good run lists items, looks up details, compares quantities, and answers from tool results only.

### 6.3 Ambiguous prompt

```bash
grok -p "We got more screws. Update inventory. Do not edit any files unless I confirm a write."
```

With the skill in play, the agent should **ask how many** (and not invent a count). Our MCP today is still read-only unless you added write tools on Day 1-that is fine. The point is judgment: clarify before guessing.

### 6.4 Optional A/B - feel the skill

Temporarily rename the skill folder so Grok cannot find it:

```bash
mv .grok/skills/warehouse-inventory .grok/skills/warehouse-inventory.off
```

Re-ask "How many hammers are in stock?" without mentioning tools. You may see more guessing or skipped tool use. Rename the folder back when you are done:

```bash
mv .grok/skills/warehouse-inventory.off .grok/skills/warehouse-inventory
```

(On Windows PowerShell, `Rename-Item` works the same way.)

## 7. What you just proved

- **One MCP server** answered both Open WebUI (Day 1) and Grok Build (Day 2).
- **One skill playbook** moved from a pasted system prompt into a skill folder the coding agent loads on its own.
- Tools give capability; skills give judgment; the client is swappable.

That pattern is what we will reuse next on **logs and pcaps**: MCP (or tools) to read evidence, plus a skill that says "do not invent the network-derive it from the artifacts."

---

**Next step:** Log and pcap analysis lab (coming next). Reconstruct a sample network from synthetic evidence.
