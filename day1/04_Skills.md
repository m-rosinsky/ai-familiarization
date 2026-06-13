# Skills

Complete [03_MCP.md](03_MCP.md) before starting this file.

## Contents

- [1. The problem: small models and tool use](#1-the-problem-small-models-and-tool-use)
- [2. What is a skill?](#2-what-is-a-skill)
- [3. Anatomy of a skill file](#3-anatomy-of-a-skill-file)
- [4. Write a warehouse skill](#4-write-a-warehouse-skill)
- [5. Load the skill in Open WebUI](#5-load-the-skill-in-open-webui)
- [6. Skills in other clients](#6-skills-in-other-clients)
- [7. Practical Exercise](#7-practical-exercise)

## 1. The problem: small models and tool use

By now you've given the model a way to reach your warehouse data twice—once as an Open WebUI **Tool** ([02_Tools.md](02_Tools.md)) and once over **MCP** ([03_MCP.md](03_MCP.md)). Wiring up the connection is only half the battle. The model still has to *decide* to use it, *pick* the right tool, and *fill in* the arguments correctly.

Large frontier models are good at this. Smaller open-weights models—like the **`llama-3.1-8b-versatile`** we run through Groq—often are not. With an 8B model you'll routinely see:

- **Skipping the tool.** You ask "how many hammers are in stock?" and it confidently makes up a number instead of calling `query_item_details`.
- **Wrong tool or wrong arguments.** It calls `query_warehouse_items` when it should look up a single item, or passes `item="hammer"` instead of `item_name="hammers"`.
- **Hallucinated results.** It calls the tool, ignores the result, and answers from memory anyway.
- **Looping or stalling.** It calls the same tool over and over, or narrates that it "will check the database" without ever doing so.

None of this means the tool is broken. The model simply wasn't steered clearly enough about *when* and *how* to use what it was given. That steering is exactly what a **skill** provides.

## 2. What is a skill?

> A **skill** is a packaged set of instructions a client loads to steer the model toward a task—when to act, which tools to reach for, and how to format the work. It's a reusable playbook, not runnable code.

You met this definition briefly in [00_Intro.md](00_Intro.md). Now we'll use it. The key idea:

- A **tool** gives the model a new *ability* (query the database).
- A **skill** gives the model *judgment* about that ability (call `query_item_details` whenever someone asks about a specific item, and never guess a quantity).

A skill is plain text. The client injects it into the model's **system context**—the same place tool definitions live (see [03_MCP.md](03_MCP.md), Section 2.1)—so it shapes behavior without ever appearing in the chat transcript. Because it's just instructions, the same skill file can be reused across clients and even across models.

This is why skills pair so well with smaller models: you can't make an 8B model bigger, but you *can* hand it a tighter playbook so it uses its tools reliably.

## 3. Anatomy of a skill file

Most clients (Cursor **Agent Skills**, Claude **Skills**, and similar) store a skill as a Markdown file with two parts:

1. **Frontmatter** — a short metadata block at the top, between `---` fences. A `name` and a `description` are the important fields. The client uses the `description` to decide *when* the skill is relevant, so write it to describe the trigger, not just the topic.
2. **Body** — the instructions themselves: what the task is, which tools to use, the rules to follow, and a few examples.

```markdown
---
name: my-skill
description: One or two sentences describing WHEN to use this skill, in terms of what the user is asking for.
---

# Title

Instructions for the model: the goal, which tools to call,
the rules to follow, and worked examples.
```

A good skill is specific and short. Vague advice ("be helpful with inventory") does nothing. Concrete triggers and rules ("when the user names a specific item, call `query_item_details` with that name; never state a quantity you didn't get from the tool") are what move the needle.

## 4. Write a warehouse skill

Let's write a skill that fixes the failure modes from Section 1 for our warehouse tools. Create a file named `warehouse_skill.md` (anywhere you like—we'll paste its contents into Open WebUI in the next section):

```markdown
---
name: warehouse-inventory-assistant
description: Use whenever the user asks about warehouse stock, quantities, item locations, or which items exist in inventory.
---

# Warehouse Inventory Assistant

You help warehouse staff check inventory. You have two tools backed by a
live SQLite database:

- `query_warehouse_items` — returns every item name in the inventory.
  Takes no arguments.
- `query_item_details` — returns the quantity and location for one item.
  Requires `item_name` (a string).

## When to use the tools

- ALWAYS call a tool for any question about stock, counts, quantities,
  locations, or which items exist. Never answer these from memory or guess
  a number.
- For "what do we have" / "list items" / "what's in the warehouse," call
  `query_warehouse_items`.
- For a specific item ("how many hammers", "where are the screwdrivers"),
  call `query_item_details` with that item's name.

## How to call the tools

- Pass `item_name` matching the user's wording; the database match is
  case-insensitive.
- If you don't know the exact item name, call `query_warehouse_items`
  first, then call `query_item_details` with a name from that list.
- Call one tool at a time and wait for its result before the next step.

## How to answer

- Base every quantity, location, and item name on the tool result you
  just received.
- If `query_item_details` reports the item wasn't found, say it isn't in
  inventory and offer to list what is. Do not invent a quantity.
- Keep answers short: state the number and location plainly.

## Examples

- User: "How many hammers are in stock?"
  → call `query_item_details(item_name="hammers")`
  → "There are 45 hammers in stock, located in Aisle 3A."
- User: "What do we carry?"
  → call `query_warehouse_items()`
  → list the names returned.
```

Notice what this does. It names the exact tools, spells out the trigger for each, pins the argument name (`item_name`), and forbids guessing. Those are precisely the things the 8B model was getting wrong on its own.

## 5. Load the skill in Open WebUI

Open WebUI doesn't have a dedicated "Skills" feature, but a skill is just instructions for the **system context**—and Open WebUI lets you set that directly. The cleanest way is to bundle the skill and the tool together as a custom **Model**, so anyone who selects it inherits both.

1. Go to **Workspace** → **Models** → **+** to create a new model.
2. Set the **Base Model** to **`llama-3.1-8b-versatile`** (the Groq model from [01_Setup.md](01_Setup.md)).
3. Give it a name like `Warehouse Assistant`.
4. Paste the **body** of `warehouse_skill.md` into the **System Prompt** field. (You can include the instructions; the `---` frontmatter is for skill-aware clients and is optional here.)
5. Under the model's **Tools** (or **Integrations**), attach the warehouse tool from [02_Tools.md](02_Tools.md) or the MCP server from [03_MCP.md](03_MCP.md).
6. **Save**, then start a **New Chat** and select your `Warehouse Assistant` model.

> Quick alternative: open the **Controls** panel inside any chat and paste the instructions into the per-chat **System Prompt** field. That works for a single conversation but isn't reusable like a saved model.

Now repeat a few of the prompts from earlier lessons—"how many hammers do we have?", "what items are in the warehouse?", "where are the measuring tapes?". With the skill in place, the model should reach for the right tool, pass the right argument, and answer from the result instead of guessing. Try toggling the system prompt off and on to feel the difference the skill makes.

## 6. Skills in other clients

The file you wrote isn't tied to Open WebUI. The same idea shows up across the ecosystem, usually as a Markdown file with the frontmatter from Section 3:

| Client | Where skills live | Notes |
|--------|-------------------|-------|
| **Cursor** | `.cursor/skills/<name>/SKILL.md` | **Agent Skills**; the agent loads one when your request matches its `description`. |
| **Claude** | Claude **Skills** | Packaged instructions (often with helper files) the model loads on demand. |
| **Open WebUI** | System Prompt on a custom Model | No native skill type; the system prompt fills the same role, as we did above. |

Because skills are plain instructions rather than code, the warehouse playbook you wrote can move between these clients with little more than a copy-paste. Pair it with the portable MCP server from [03_MCP.md](03_MCP.md) and you have a tool *and* the judgment to use it, both reusable across apps.

## 7. Practical Exercise

Extend your warehouse skill to handle the write operations you added in the [02_Tools.md](02_Tools.md) exercise (update, add, remove items):

- Add rules for **when** to call each write tool versus a read tool.
- Require the model to **confirm** a change with the user before removing an item or setting a quantity to zero.
- Tell it to **read back** the new value (via `query_item_details`) after a write so the user sees the result.
- Test a deliberately ambiguous prompt like "we got more screws"—does the skill make the model ask how many, rather than guessing?

---

**Next step:** [05_Loops.md](05_Loops.md). Put tools, MCP, and your skill together and watch the model chain several calls into an agent loop.
