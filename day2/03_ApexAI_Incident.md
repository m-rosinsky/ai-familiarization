# ApexAI Incident Investigation

Complete [02_MCP_Skills.md](02_MCP_Skills.md) before starting this file. You need a working Grok Build session from [01_Setup.md](01_Setup.md).

## Scenario

**ApexAI** is a fictional company that suffered a cyber attack. Security collected logs and packet captures from the incident window. There is no network diagram in the ticket.

Your job is to use AI tools (Grok Build, plus search/`tshark` as needed) to investigate the evidence and figure out what the network looks like and what happened.

Evidence is in [`network_logs/`](../network_logs/) at the repo root (five `.log` files and three `.pcap` files). All of it is synthetic training data.

## Deliverables

Produce two artifacts (markdown is fine):

1. **Network map** - zones, key hosts/IPs, and how they connect, based on the evidence.
2. **Incident summary** - what occurred, in order, with enough detail that someone else can follow the story from the logs and pcaps.

Base claims on the files in `network_logs/`. Do not invent hosts, events, or IOCs that are not supported by the evidence.

## Getting started

From the repo root, with your class `XAI_API_KEY` set:

```bash
cd ai-familiarization
grok
```

Point Grok at `network_logs/` and investigate. Skills are optional but encouraged - you practiced them on Day 1 and in [02_MCP_Skills.md](02_MCP_Skills.md); writing your own under `.grok/skills/` can help keep the agent honest (cite sources, do not guess).

When the class debriefs, compare your map and summary with the instructor’s answer key (not included in this repo).
