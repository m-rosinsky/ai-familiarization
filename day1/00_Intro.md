# Introduction

Start here before [01_Setup.md](01_Setup.md). We'll walk through the words and ideas you'll keep seeing for the rest of Day 1.

## Contents

- [1. What is a model?](#1-what-is-a-model)
- [2. Models in the wild](#2-models-in-the-wild)
- [3. What is an AI client?](#3-what-is-an-ai-client)
- [4. Hosting: where the model runs](#4-hosting-where-the-model-runs)
- [5. Terminology you'll see in this course](#5-terminology-youll-see-in-this-course)

## 1. What is a model?

> A **model** (usually an **LLM**, or large language model) is a trained neural network that reads a prompt and generates a response.

Think of it as the brain. On its own, it can't browse the web, query your database, or edit files. Something else has to give it those abilities.

Say you ask *"How many hammers are in stock?"* The model guesses the next words that best fit your question and what it learned during training. It doesn't magically know about your warehouse. It only knows what was in its training data plus whatever you put in the current chat.

In this course we use **`llama-3.1-8b-versatile`** through Groq: an open Llama model, running on Groq's servers, that you talk to through Open WebUI.

## 2. Models in the wild

Lots of companies train models or host them for you. They vary in size, speed, cost, and how smart they feel. You don't need to memorize every name. Just know who's out there.

| Provider | Example models | Notes |
|----------|----------------|-------|
| **OpenAI** | GPT-4o, o-series | ChatGPT and APIs; strong all-around reasoning |
| **Anthropic** | Claude Sonnet, Opus, Haiku | Claude apps and Claude Code; great at code and long docs |
| **Google** | Gemini | Tied into Google Workspace and Vertex AI |
| **Meta** | Llama 3.x | Open weights; often run locally or via Groq, Together, Ollama |
| **Mistral** | Mistral Large, Codestral | Popular for APIs and self-hosted setups |
| **xAI** | Grok | Powers Grok on X and Grok Build |
| **Groq** (this course) | Hosts Llama, Mixtral, etc. | An **inference provider**, not a model lab. They run open models fast on their own hardware |

**Proprietary vs open-weights:** Models like GPT-4 and Claude you only reach through the vendor's app or API. Open-weights models like Llama can be downloaded and run on your machine with [Ollama](https://ollama.com/), or hosted by someone like Groq.

**Picking a model:** Bigger models usually reason better, but they cost more and feel slower. Smaller ones (like the 8B Llama we use) are plenty for learning and plenty of real work. Teams often mix and match: something quick for easy questions, something heavier for hard ones.

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

## 4. Hosting: where the model runs

| Mode | Meaning | Example in this course |
|------|---------|------------------------|
| **Cloud / API** | The model runs on someone else's servers. You send prompts over the internet. | Groq runs Llama; Open WebUI sends requests with your API key. |
| **Local** | The model runs on your machine. | Ollama with Llama on your laptop. No API key, but you need decent hardware. |
| **Hybrid** | The app is local; the model is remote. | Open WebUI Desktop on your PC, Groq in the cloud. That's our setup. |

Running locally keeps more data on your machine, but bigger models want a good GPU. Cloud is easier to get started with, so that's what we use on Day 1.

## 5. Terminology you'll see in this course

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
