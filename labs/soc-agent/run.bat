@echo off
set OLLAMA_HOST=http://172.16.2.10:11434
set OLLAMA_MODEL=apex-llama
set PCAP_ROOT=C:\labs\pcaps
cd /d C:\labs\soc-agent
python agent.py %*
