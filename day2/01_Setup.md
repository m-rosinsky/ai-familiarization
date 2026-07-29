# Setup

Complete [Day 1](../day1/README.md) before starting this file.

## What we're installing

On Day 1 you used **Open WebUI**: a desktop chat client pointed at Groq. Today we switch clients.

**Grok Build** is xAI's coding agent. You run it from a terminal as the `grok` command. It can open an interactive session in your project folder, edit files, run commands, and (later today) load the same kinds of **MCP** servers and **skills** you met on Day 1.

Same ideas. Different shell around the model.

Official docs: [Grok Build overview](https://docs.x.ai/build/overview).

## Install the Grok CLI

Pick the installer for your shell. Both put a `grok` binary on your `PATH`.

**macOS / Linux / Git Bash / WSL**

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

**Windows (PowerShell)**

```powershell
irm https://x.ai/cli/install.ps1 | iex
```

> If the PowerShell installer is blocked in your environment, the npm fallback works on every OS that has Node.js: `npm install -g @xai-official/grok`.

Open a **new** terminal window so your `PATH` refreshes, then verify:

```bash
grok --version
```

You should see a version string (for example `0.1.x`). If the command is not found, the install location is not on your `PATH`-re-open the terminal, or add the directory the installer printed to your shell profile and try again.

## Get the class API key

This class uses **one shared enterprise key** for Grok Build. You do **not** create your own key at [console.x.ai](https://console.x.ai/).

> Do not commit the key to git, paste it into a prompt, or check it into this repo (including `.env` files you might push later).

> **Warning:** Everyone in the room shares the same quota. Stick to the course outline-avoid long free-form chats or unrelated experiments, or the class can burn through the limit before the labs are done.

## Authenticate

Grok Build reads the class key from the `XAI_API_KEY` environment variable. Set it in the terminal where you will run `grok`.

**macOS / Linux / Git Bash / WSL**

```bash
export XAI_API_KEY="xai-..."
```

**Windows (PowerShell)**

```powershell
$env:XAI_API_KEY = "xai-..."
```

Replace `xai-...` with the key your instructor gave you.

That setting lasts for the current terminal session only. Close the window and you will need to set it again-unless you persist it (next section).

### Optional: persist the key in config

So you do not re-export the key every lab, you can bind it in Grok's user config.

Config file path:

- **macOS / Linux:** `~/.grok/config.toml`
- **Windows:** `%USERPROFILE%\.grok\config.toml` (same idea: a `.grok` folder under your home directory)

Create the folder if needed, then create or edit `config.toml` so it includes:

```toml
[model.grok-build]
api_key = "xai-..."

[models]
default = "grok-build"
```

Use the real class key in place of `xai-...`.

> Prefer the environment variable during class if you are unsure about editing config files. Either path is fine for the smoke test below.

## Smoke test

From a terminal where `XAI_API_KEY` is set (or where the config file has the key), go to this repo:

```bash
cd ai-familiarization
```

(Use the path where you cloned the repo on Day 1.)

Send one headless prompt-no interactive TUI required:

```bash
grok -p "In five short bullets, explain what this repository is for. Do not edit any files."
```

You should get a short summary that mentions Day 1 / Day 2 labs (or similar). That confirms:

1. `grok` is installed.
2. Auth works with the class key.
3. The agent can see the project folder.

Optional checks:

```bash
grok inspect
```

`grok inspect` prints what Grok discovered in the current directory (config sources, and later skills / MCP). Handy when something looks wrong.

To open the interactive session instead of a one-shot prompt:

```bash
grok
```

Exit when you are done (follow the on-screen quit hint, often `Ctrl+C` or a `/quit`-style command depending on build).

## You're ready

Grok Build is installed and talking to xAI with the class key.

**Next step:** [02_MCP_Skills.md](02_MCP_Skills.md). Point this coding agent at the Day 1 warehouse MCP and skill.
