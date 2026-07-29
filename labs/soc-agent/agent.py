"""Minimal SOC harness: chat + Ollama tools (PCAP summarize).

Usage:
  set OLLAMA_HOST=http://172.16.2.10:11434
  python agent.py
  python agent.py path\\to\\lab1.pcap
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import urllib.request

OLLAMA = os.environ.get("OLLAMA_HOST", "http://172.16.2.10:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "apex-llama")
PCAP_ROOT = Path(os.environ.get("PCAP_ROOT", r"C:\labs\pcaps")).resolve()

SYSTEM = """You are a blue-team assistant on an isolated range.
Use tools when evidence is on disk. Quote tool output; do not invent packets.
If the user names a pcap, call analyze_pcap with that filename only (no paths outside the lab folder).
Keep answers short: findings, evidence quotes, next checks."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "analyze_pcap",
            "description": "Summarize a PCAP in the lab folder (protocols, top talkers, DNS/HTTP hints).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "File name only, e.g. lab1.pcap",
                    }
                },
                "required": ["filename"],
            },
        },
    }
]


def _post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{OLLAMA}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read().decode())


def analyze_pcap(filename: str) -> str:
    name = Path(filename).name
    if name != filename or ".." in filename:
        return "ERROR: filename only, no paths."
    path = (PCAP_ROOT / name).resolve()
    if not str(path).startswith(str(PCAP_ROOT)) or not path.is_file():
        return f"ERROR: not found under {PCAP_ROOT}: {name}"

    cmds = [
        ["tshark", "-r", str(path), "-q", "-z", "io,phs"],
        ["tshark", "-r", str(path), "-q", "-z", "conv,ip"],
        [
            "tshark",
            "-r",
            str(path),
            "-Y",
            "dns.qry.name",
            "-T",
            "fields",
            "-e",
            "dns.qry.name",
        ],
    ]
    chunks: list[str] = []
    for cmd in cmds:
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False)
            text = (out.stdout or out.stderr or "").strip()
            chunks.append(f"$ {' '.join(cmd)}\n{text[:4000]}")
        except FileNotFoundError:
            return "ERROR: tshark not installed or not on PATH."
        except Exception as e:
            chunks.append(f"$ {' '.join(cmd)}\nERROR: {e}")
    return "\n\n".join(chunks)[:12000]


TOOL_IMPL = {"analyze_pcap": lambda args: analyze_pcap(args.get("filename", ""))}


def chat(messages: list[dict]) -> dict:
    return _post(
        "/api/chat",
        {"model": MODEL, "messages": messages, "tools": TOOLS, "stream": False},
    )


def run_turn(messages: list[dict], user_text: str) -> str:
    messages.append({"role": "user", "content": user_text})
    for _ in range(4):
        msg = chat(messages).get("message") or {}
        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            content = msg.get("content") or ""
            messages.append({"role": "assistant", "content": content})
            return content

        messages.append(msg)
        for call in tool_calls:
            fn = call.get("function") or {}
            name = fn.get("name") or ""
            raw_args = fn.get("arguments") or {}
            if isinstance(raw_args, str):
                try:
                    raw_args = json.loads(raw_args)
                except json.JSONDecodeError:
                    raw_args = {}
            result = TOOL_IMPL.get(name, lambda _: f"ERROR: unknown tool {name}")(raw_args)
            messages.append({"role": "tool", "content": result})
    return "Stopped: too many tool iterations."


def main() -> None:
    PCAP_ROOT.mkdir(parents=True, exist_ok=True)
    messages: list[dict] = [{"role": "system", "content": SYSTEM}]
    print(f"Ollama={OLLAMA} model={MODEL} pcaps={PCAP_ROOT}")
    print("Type a question (or /quit). Example: Summarize lab1.pcap\n")

    if len(sys.argv) > 1:
        print(run_turn(messages, f"Analyze this pcap and report suspicious activity: {Path(sys.argv[1]).name}"))
        return

    while True:
        try:
            line = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line or line in {"/q", "/quit", "exit"}:
            break
        print("agent>", run_turn(messages, line), "\n")


if __name__ == "__main__":
    main()
