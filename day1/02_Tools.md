# Tools

Complete [01_Setup.md](01_Setup.md) before starting this file.

## Contents

- [1. What is an AI Tool?](#1-what-is-an-ai-tool)
- [2. Setting up our local database](#2-setting-up-our-local-database)
- [3. Query the database manually](#3-query-the-database-manually)
  - [3.1 Install the SQLite CLI](#31-install-the-sqlite-cli)
  - [3.2 Run queries with SQLite](#32-run-queries-with-sqlite)

## 1. What is an AI Tool?

> A specific executable function or API that an AI model can call to interact with the outside world, perform calculations, or fetch data (e.g., a web search tool, a calculator, or a file-writer). The model decides when to use it based on your prompt.

We want our AI to query and update a local warehouse inventory database—not just answer from memory.

To do this, we'll supply our AI with a Tool that tells it how and when to interact with the database. First, set up the database and verify it manually.

## 2. Setting up our local database

Set up a locally hosted database using Python and SQLite.

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

## 3. Query the database manually

Before wiring the database up to the AI, connect locally and run a few queries yourself. This confirms the data is there and shows what the AI will be working with.

### 3.1 Install the SQLite CLI

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

### 3.2 Run queries with SQLite

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
