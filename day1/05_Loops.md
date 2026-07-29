# Loops

Complete [04_Skills.md](04_Skills.md) before starting this file. This is the last stop on Day 1, and it ties everything else together.

## Contents

- [1. From one tool call to many](#1-from-one-tool-call-to-many)
- [2. What is an agent loop?](#2-what-is-an-agent-loop)
- [3. The loop, step by step](#3-the-loop-step-by-step)
- [4. Watch it happen in Open WebUI](#4-watch-it-happen-in-open-webui)
- [5. When the loop goes wrong](#5-when-the-loop-goes-wrong)
- [6. So what is an "agent"?](#6-so-what-is-an-agent)
- [7. Practical Exercise](#7-practical-exercise)

## 1. From one tool call to many

Every question you've asked so far needed exactly one tool call. "How many hammers?" → one `query_item_details` → an answer. But real tasks rarely fit in a single step.

Ask instead: **"Which item do we have the fewest of, and where is it?"**

Our tools can't answer that in one shot. `query_warehouse_items` returns names but no quantities. `query_item_details` returns the quantity for *one* item. To answer, the model has to:

1. Get the list of items.
2. Look up the quantity for each one.
3. Compare the results.
4. Report the smallest, with its location.

That's four tool calls plus some reasoning, all driven by a single prompt. The mechanism that makes this possible is the **loop**.

## 2. What is an agent loop?

> An **agent loop** is the cycle where the model proposes an action, the client runs it, the result is fed back to the model, and the cycle repeats until the model has enough to answer.

You saw the one-line version in [00_Intro.md](00_Intro.md). Here's the important nuance: **the model never runs anything itself.** Just like in the MCP exchange from [03_MCP.md](03_MCP.md), the model only *suggests* a tool call. The **client** (Open WebUI) is what actually executes it and hands the result back.

The cycle has three beats:

```text
   ┌──────────────────────────────────────────────┐
   │                                                │
   ▼                                                │
[ model proposes ] → [ client runs ] → [ result back ]
   (think/act)         the tool          to the model
   │                                                ▲
   │  no more tools needed?                         │
   └────────────► [ final answer ] ─────────────────┘
```

Plan, act, observe-then decide whether to loop again or stop. Tools and MCP ([02_Tools.md](02_Tools.md), [03_MCP.md](03_MCP.md)) are what give the loop something to *do*; the skill ([04_Skills.md](04_Skills.md)) is what keeps it on track.

## 3. The loop, step by step

Here's what the client and model actually pass back and forth for "which item do we have the fewest of, and where is it?" against our seeded database (`hammers` 45, `screwdrivers` 120, `screws (100pk)` 350, `measuring tapes` 18).

| Turn | Who | What happens |
|------|-----|--------------|
| 1 | **You** | "Which item do we have the fewest of, and where is it?" |
| 2 | **Model** | "I don't know the items yet." Proposes `query_warehouse_items()`. |
| 3 | **Client** | Runs the tool. Returns `["hammers", "measuring tapes", "screwdrivers", "screws (100pk)"]`. |
| 4 | **Model** | "Now I need each quantity." Proposes `query_item_details(item_name="hammers")`. |
| 5 | **Client** | Returns `Item: hammers \| Quantity in stock: 45 \| Location: Aisle 3A`. |
| 6 | **Model** | Proposes `query_item_details(item_name="measuring tapes")`. |
| 7 | **Client** | Returns `... Quantity in stock: 18 \| Location: Aisle 2A`. |
| 8-11 | **Model + Client** | Repeats for `screwdrivers` (120) and `screws (100pk)` (350). |
| 12 | **Model** | Has all four quantities. No more tools needed. Compares: 18 is smallest. |
| 13 | **Model** | Final answer: "We have the fewest measuring tapes-18 in stock, in Aisle 2A." |

Notice turn 12: the loop ends when the model decides it has enough information, not because the client told it to stop. Each tool result became part of the context the model used to plan its next move. The same prompt, asked of a database with different data, would loop a different number of times.

## 4. Watch it happen in Open WebUI

You don't need to write any new code-your tool (or MCP server) from the earlier lessons already supports this. Use the `Warehouse Assistant` model you set up in [04_Skills.md](04_Skills.md) (or any chat with the warehouse tool enabled) and try:

```text
Which item do we have the fewest of, and where is it?
```

While it works, expand the tool-call details in the response. Open WebUI shows each call the model made and the result it got back. You should see several calls stack up-one to list items, then one per item-before the final sentence. That stack *is* the loop.

A few more prompts that force multiple steps:

- "What's our total quantity across every item?"
- "List every item stored in an Aisle 3 location."
- "Do we have more screwdrivers than hammers?"

Each one requires the model to gather several results and reason over them, rather than echoing a single lookup.

## 5. When the loop goes wrong

Open loops are where smaller models struggle most, because every extra step is another chance to slip. Watch for the failure modes from [04_Skills.md](04_Skills.md), now stretched across multiple turns:

- **Stopping too early.** It lists the items, then guesses the smallest without looking up quantities.
- **Never stopping.** It keeps calling the same tool, or re-lists items it already has, without converging on an answer.
- **Losing the thread.** It gathers quantities but forgets the original question and reports the wrong item.

This is exactly why we wrote the skill before this lesson. Rules like *"call one tool at a time and wait for its result"* and *"base every quantity on the tool result you just received"* are guardrails for the loop. Try the prompt with the system prompt on, then off, and watch how much more reliably the loop completes with the skill steering it.

> A bigger model loops more reliably on its own. A smaller model needs a good skill to loop well. Same loop, different amount of hand-holding.

## 6. So what is an "agent"?

You now have every piece behind the industry's favorite buzzword.

> An **agent** is a model running in a loop with access to tools, taking multiple steps to accomplish a goal.

Strip away the marketing and an "agent" is just what you've already built:

- a **model** ([00_Intro.md](00_Intro.md)) -
- reached through a **client** ([01_Setup.md](01_Setup.md)) -
- given **tools** ([02_Tools.md](02_Tools.md)), optionally over **MCP** ([03_MCP.md](03_MCP.md)) -
- steered by a **skill** ([04_Skills.md](04_Skills.md)) -
- running in a **loop** (this file).

When a product calls itself an "AI agent," this is the machinery underneath. The warehouse assistant you built is a small but genuine agent: it plans, acts, observes, and repeats until your question is answered.

## 7. Practical Exercise

Push the loop further using the write tools you added in the [02_Tools.md](02_Tools.md) and [04_Skills.md](04_Skills.md) exercises:

- Prompt a multi-step task: *"If we have fewer than 20 of anything, order 50 more of it."* The model should list items, check each quantity, update the low ones, and report what it changed.
- Count the tool calls in the response. How many turns did the loop take?
- Add a rule to your skill that caps how the model works (for example, "look up each item only once") and see whether it makes the loop tighter.
- Try a prompt with **no** matching items (*"order more of anything below zero"*) and confirm the loop ends cleanly instead of spinning.
