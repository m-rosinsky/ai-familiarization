# Day 1: AI Concepts

## Contents

- [1. Purpose](#1-purpose)
- [2. Setup](#2-setup)
  - [2.1 Get a Groq API key](#21-get-a-groq-api-key)
  - [2.2 Download Open WebUI Desktop](#22-download-open-webui-desktop)
  - [2.3 Launch and first-time setup](#23-launch-and-first-time-setup)
- [3. Tools](#3-tools)
  - [3.a. Setting up our local database](#3a-setting-up-our-local-database)
  - [3.b. Query the database manually](#3b-query-the-database-manually)

## 1. Purpose

Students will become familiar with the following concepts of modern AI usage:

- Local and hybrid-hosted models
- Tools
- MCPs
- Skills
- Loops

## 2. Setup

### 2.1 Get a Groq API key

Open WebUI will use [Groq](https://groq.com/) to run cloud-hosted models. Groq offers a free tier and does not require a credit card.

1. Go to the [Groq Console](https://console.groq.com/) and sign up with email, Google, or GitHub.
2. Verify your email if prompted.
3. Open [**API Keys**](https://console.groq.com/keys) in the left sidebar.
4. Click **Create API Key**, give it a name (for example, `open-webui`), and click **Submit**.
5. Copy the key immediately. It starts with `gsk_` and is only shown once. If you lose it, create a new key.

Keep the key somewhere safe for the next section. You will paste it into Open WebUI in step 6 of [§2.3](#23-launch-and-first-time-setup).

> Do not commit your API key to git or share it publicly.

> **Warning:** Groq's free tier provides enough tokens to get you through this class, but it has daily rate limits. Stick to the course outline—avoid extra experimentation or unrelated prompts, or you may hit your limit before the course is over.

### 2.2 Download Open WebUI Desktop

Go to the [Open WebUI Desktop download page](https://github.com/open-webui/desktop#download) and install the build for your platform.

### 2.3 Launch and first-time setup

1. Open **Open WebUI** from your applications menu or Start menu.
2. Select the option to **Run Locally**.
3. Select the **Open WebUI** connection on the left and create a local admin account:

| ![image2_1.png](../imgs/image2_1.png) |
|:--:|
| _Create a local admin account_ |

4. You should now see the chat input area:

| ![image2_2.png](../imgs/image2_2.png) |
|:--:|
| _Verify Open WebUI_ |

5. Open **Settings** by clicking your profile icon → **Settings**:

| ![image2_3.png](../imgs/image2_3.png) |
|:--:|
| _Open settings_ |

6. Under **OpenAI API** → **Manage OpenAI API Connections**, click the **+** button.

   - Set URL to:

     ```text
     https://api.groq.com/openai/v1
     ```

   - Under **Auth**, select **Bearer**
   - Paste your Groq API key
   - Press **Save**

| ![image2_4.png](../imgs/image2_4.png) |
|:--:|
| _Configure Groq connection_ |

7. Press **New Chat**. You should now see a dropdown of models in the upper-left corner:

   - Select **`llama-3.1-8b-instant`**

| ![image2_5.png](../imgs/image2_5.png) |
|:--:|
| _Validate models appear_ |

8. Send a test prompt and verify the model responds:

| ![image2_6.png](../imgs/image2_6.png) |
|:--:|
| _Test model response_ |

## 3. Tools

Definition:
> A specific executable function or API that an AI model can call to interact with the outside world, perform calculations, or fetch data (e.g., a web search tool, a calculator, or a file-writer). The model decides when to use it based on your prompt.

### 3.a. Setting up our local database

We want our AI to query and update a local warehouse inventory database—not just answer from memory.

In order to do this, we'll need to supply our AI with a Tool, which tells it how and when to interact with the database.

First, let's set up a locally hosted database using Python and Sqlite.

From the repo root, run:

```bash
cd inventory_db
python init_db.py
```

This creates `warehouse.db` in `inventory_db/` with an `inventory` table (item name, quantity, location) and seeds it with sample hardware-store stock.

You should see:

```text
Database initialized successfully with inventory data!
```

Re-running the script is safe, it won't duplicate existing rows.

### 3.b. Query the database manually

Before wiring the database up to the AI, connect locally and run a few queries yourself. This confirms the data is there and shows what the AI will be working with.

#### Install the SQLite CLI

Check whether `sqlite3` is already available:

```bash
sqlite3 --version
```

If that fails, install it for your platform:

**Windows:**

```bash
winget install SQLite.SQLite
```

**macOS:**

```bash
brew install sqlite
```

**Linux (Debian / Ubuntu):**

```bash
sudo apt update
sudo apt install sqlite3
```

**Linux (Fedora):**

```bash
sudo dnf install sqlite
```

#### Run queries with SQLite

From `inventory_db/`:

```bash
sqlite3 warehouse.db
```

At the `sqlite>` prompt:

```sql
.tables
SELECT * FROM inventory;
SELECT quantity, location FROM inventory WHERE item_name = 'hammers';
```

Exit with `.quit`.

| ![image3_1.png](../imgs/image3_1.png) |
|:--:|
| _Manual sqlite querying_ |
