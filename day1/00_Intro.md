# Introduction

Start here before [01_Setup.md](01_Setup.md). We'll walk through the words and ideas you'll keep seeing for the rest of Day 1.

## Contents

- [1. What is a model?](#1-what-is-a-model)
- [2. Models in the wild](#2-models-in-the-wild)
  - [2.1 Model size and naming](#21-model-size-and-naming)
- [3. What is an AI client?](#3-what-is-an-ai-client)
- [4. Types of AI applications](#4-types-of-ai-applications)
- [5. Hosting: where the model runs](#5-hosting-where-the-model-runs)
- [6. Terminology you'll see in this course](#6-terminology-youll-see-in-this-course)

## 1. What is a model?

> A **model** (usually an **LLM**, or large language model) is a trained neural network that reads a prompt and generates a response.

In this course we use **`llama-3.3-70b-versatile`** through Groq: an open Llama model, running on Groq's servers, that you talk to through Open WebUI.

## 2. Models in the wild

Lots of companies train models or host them for you. They vary in size, speed, cost, and how smart they feel. You don't need to memorize every name. Just know who's out there.

### 2.1 Model size and naming

> **Model size** usually means how many **parameters** the model has: the internal weights it learned during training.

You'll see shorthand like **8B**, **70B**, or **1T**:

| Shorthand | Means | Example |
|-----------|--------|---------|
| **B** | Billion parameters | **8B** = 8 billion; **70B** = 70 billion (our course model) |
| **M** | Million parameters | Smaller or specialized models |
| **T** | Trillion parameters | **1T model** = about one trillion parameters |

When someone says *"a 1T model,"* they mean a very large network with on the order of a trillion parameters. More parameters often means stronger reasoning and broader knowledge, but also more compute, higher cost, and slower responses. Not every headline number tells the whole story: some models advertise **total** parameters while only a **subset** is "active" on each request (a **mixture-of-experts**, or MoE, design). The label on the tin and how it behaves in practice can differ.

Names like **`llama-3.3-70b-versatile`** encode useful hints: **Llama** (family), **3.3** (version), **70b** (70 billion parameters), **versatile** (what the host tuned it for). Bigger is not always better for your job; a 70B model is a strong default for learning and many everyday tasks.

| Provider | Example models | Notes |
|----------|----------------|-------|
| **OpenAI** | GPT-4o, o-series, Codex | ChatGPT and APIs; strong all-around reasoning |
| **Anthropic** | Claude Sonnet, Opus, Haiku | Claude apps and Claude Code; great at code and long docs |
| **Google** | Gemini | Tied into Google Workspace and Vertex AI |
| **Meta** | Llama 3.x | Open weights; often run locally or via Groq, Together, Ollama |
| **Mistral** | Mistral Large, Codestral | Popular for APIs and self-hosted setups |
| **xAI** | Grok | Powers Grok on X and Grok Build |
| **Groq** (this course) | Hosts Llama, Mixtral, etc. | An **inference provider**, not a model lab. They run open models fast on their own hardware |
| **Cursor** | Composer series | Cursor is mostly known for their IDE of the same name, but also develops the Composer models |

**Proprietary vs open-weights:** Models like GPT-4 and Claude you only reach through the vendor's app or API. Open-weights models like Llama can be downloaded and run on your machine with [Ollama](https://ollama.com/), or hosted by someone like Groq.

**Picking a model:** Bigger models usually reason better, but they cost more and feel slower. A mid-size model (like the 70B Llama we use) is a good balance for learning and plenty of real work. Teams often mix and match: something quick for easy questions, something heavier for hard ones.

## 3. What is an AI client?

> An **AI client** (also called a **host** or **AI app**) is the application you use to send prompts to a model and receive its replies.

It can also layer on **tools**, **MCP servers**, files, and project context. The model and the client are not the same thing. One model can show up in many clients. One client can be pointed at different models or providers.

| Client | What it is |
|--------|------------|
| **[Open WebUI](https://openwebui.com/)** | A chat UI you run yourself (we use Desktop in this course). Hooks up to Groq in the cloud or to local runners like Ollama. |
| **[Cursor](https://cursor.com/)** | A code editor built around AI: chat, autocomplete, and agents inside your repo. |
| **Claude Code / Claude Desktop** | Anthropic's CLI and desktop apps for coding and general chat. |
| **ChatGPT** | OpenAI's chat product for consumers and teams. |
| **Grok Build** | xAI's setup for building with Grok models and tools. |
| **VS Code + Copilot, Windsurf, etc.** | Same pattern: an editor plus a model plus optional tools. |

**Provider vs client:** Groq, OpenAI, and Anthropic are **providers**. They run the model and offer an API. Open WebUI and Cursor are **clients**. They call those APIs for you. You can change providers without switching apps, which is exactly what we do when we point Open WebUI at Groq.

## 4. Types of AI applications

> An **AI application** is software built for a particular way of working with a model: chatting in a window, editing a repo, running tasks from a terminal, and so on.

The model might be the same underneath. What changes is the interface, the context the app can see, and how much it can do on your behalf.

| Type | Where you work | What it's good at | Examples |
|------|----------------|-------------------|----------|
| **Web chat** | Browser | General Q&A, documents, light tool use | ChatGPT (web), Open WebUI in a browser |
| **Desktop app** | Native app on your OS | Same as chat, plus tighter OS integration (files, shortcuts) | Open WebUI Desktop, Claude Desktop |
| **IDE** | Inside a code editor | Writing and refactoring code, repo-aware chat, inline suggestions | Cursor, Windsurf, VS Code + Copilot |
| **CLI** | Terminal | Scriptable workflows, automation, coding tasks without a GUI | Claude Code, Cursor Agent, OpenAI Codex CLI |
| **Build / agent platforms** | Vendor-specific UI | Multi-step tasks, connectors, prototyping full workflows | Grok Build, OpenAI Agent Builder |

A few patterns worth knowing:

- **One company, many shapes.** Anthropic ships Claude Desktop (app) and Claude Code (CLI). Cursor is an IDE first, but Cursor Agent runs from the terminal too. Same provider, different shells around the model.
- **Context follows the app.** A chat app mostly sees your conversation. An IDE sees open files and your project tree. A CLI agent can be pointed at a folder and wired into scripts or CI. More context usually means better answers for that kind of work.
- **Agents show up everywhere.** "Agent" in the product name often means the app can loop: plan, call tools, edit files, and keep going until a task is done. That behavior can live in an IDE, a desktop app, or a CLI.

For Day 1 we use **Open WebUI Desktop**: a desktop chat app that connects to a cloud model (Groq) and can attach **tools** and **MCP servers**. Later you can reuse the same MCP server from Cursor or other clients without rewriting it.

## 5. Hosting: where the model runs

| Mode | Meaning | Example in this course |
|------|---------|------------------------|
| **Cloud / API** | The model runs on someone else's servers. You send prompts over the internet. | Groq runs Llama; Open WebUI sends requests with your API key. |
| **Local** | The model runs on your machine. | Ollama with Llama on your laptop. No API key, but you need decent hardware. |
| **Hybrid** | The app is local; the model is remote. | Open WebUI Desktop on your PC, Groq in the cloud. That's our setup. |

Running locally keeps more data on your machine, but bigger models want a good GPU. Cloud is easier to get started with, so that's what we use on Day 1.

## 6. Terminology you'll see in this course

### Prompt and context

- **Prompt:** The text you send the model. Your question or instruction.
- **System prompt / system context:** Instructions the client adds before your messages, often hidden from the chat UI. Things like "You are a helpful assistant" or a list of tools the model can use. This is not the same as the back-and-forth in the chat window.
- **Token:** A small piece of text the model reads and writes. Usage limits and pricing are usually counted in tokens.
- **Context window:** How much text the model can take in at once: your conversation, system context, tool results, all combined.

### Capabilities we build in Day 1

- **Tool:** A function the model can call, like querying a SQLite database. We build one in [02_Tools.md](02_Tools.md).
- **MCP (Model Context Protocol):** A shared standard for exposing tools and data so any compatible client can use them. We cover this in [03_MCP.md](03_MCP.md).
- **Skill:** Packaged instructions some clients load to steer the model (Cursor **Agent Skills**, Claude **Skills**, and similar). A reusable playbook, not runnable code on its own.
- **Loop / agent loop:** The model suggests an action, the client runs it, the result goes back to the model, and that repeats until the job is done or the model replies. Tools and MCP are what make that loop actually useful.

### Other useful terms

- **Inference:** Running the model on a prompt to get an answer. Different from *training*, which is how the model was built in the first place.
- **Hallucination:** When the model sounds sure about something that's wrong or made up. Tools and MCP help on factual questions by tying answers to real data.
- **RAG (retrieval-augmented generation):** Pull in relevant documents first, then ask the model to answer from them. Related to tools, but focused on searching a knowledge base.
- **Agent:** Often means an LLM in a loop that can use tools over several steps. Marketing uses the word loosely. Under the hood it's still model + client + tools.

---

**Next step:** [01_Setup.md](01_Setup.md). Install Open WebUI, grab a Groq API key, and send your first prompt.
