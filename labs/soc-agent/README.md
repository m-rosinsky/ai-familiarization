# SOC agent harness for ApexFlow (dev box → apex-llm)

## On the golden Dev box (once, offline-friendly)

1. Stage via LAE File Management onto the VM:
   - Python 3 embeddable/installer (Windows) or `.deb` (Linux)
   - Wireshark/tshark installer (includes `tshark`)
   - this folder: `agent.py`
   - sample pcaps into `C:\labs\pcaps\` (Windows) or `/opt/labs/pcaps` (Linux)

2. Install Python + tshark. Confirm:
   ```text
   python --version
   tshark -v
   ```

3. Env (persist in System env or a `run.bat`):
   ```text
   OLLAMA_HOST=http://172.16.2.10:11434
   OLLAMA_MODEL=apex-llama
   PCAP_ROOT=C:\labs\pcaps
   ```

4. Run:
   ```text
   cd C:\labs\soc-agent
   python agent.py
   ```
   Or: `python agent.py lab1.pcap`

5. Sanity: from same box, `Invoke-RestMethod http://172.16.2.10:11434/api/tags` still works.

No pip packages required (`urllib` only). Optional later: richer parsers.

## Clone to ~12 student boxes (PCTE)

When Dev is golden (static `/24` IP pattern, Python, tshark, `C:\labs\...`, agent runs):

1. Shut down the golden Dev VM cleanly.
2. Ranges → Manage Deployment → that VM → **Download** → **Save as Template**  
   e.g. `ApexFlow-Dev-SOC-Agent`.
3. Draft network spec: create `dev-01` … `dev-12` (or duplicate the VM).
4. Each Dev VM:
   - Template: `ApexFlow-Dev-SOC-Agent`
   - **Start Only** (IPs/tools already baked) **or** Start+Configure with `windows_nic::ip` **/24** + unique address `172.16.3.10+N`
   - Unique MAC + unique in-band IP per seat
   - Same modules pattern that finally worked on `dev-01` (mask `/24`, gateway `172.16.3.1`)
5. Commit → deploy / refresh **clone source** of the full range.
6. Spot-check 2 seats: `ping 172.16.2.10`, `python agent.py`.

Do **not** give all 12 the same IP. Template clones software; Networking tab (or Puppet NIC) must assign **per-VM** addresses.
