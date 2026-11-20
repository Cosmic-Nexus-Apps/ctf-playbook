# ctf-playbook

A reusable, opinionated playbook for **box-style CTF competitions**: multi-service vulnerable
machines with web apps, APIs, LLM agents, SSRF, JWT, drones/MAVLink, steganography and forensics.

It captures the exact techniques that worked in real competitions (starting with the official
CTF-USV 2026 "DUNE" writeup) and the anti-rabbit-hole rules that save hours.

## What is inside

- **Methodology**: recon, web patterns, LLM prompt injection, SSRF chains, MAVLink signing,
  forensics, per-service checklist.
- **Prompt-injection recipes**: system-prompt extraction, authority framing ("end of document"),
  chunked extraction, and the *modified-value* trick that defeats exact-string redaction.
- **Scripts**: JWT forge, LLM petition sender, page-ID/base64 enumerator, signed MAVLink flight.
- **Case study**: a sanitized walkthrough of CTF-USV 2026 (credentials and flags removed).

## Install

As an agent skill (recommended):

```bash
npx skills add Cosmic-Nexus-Apps/ctf-playbook@ctf-playbook -g -y
```

Manual: copy the `ctf-playbook/` directory into your agent's skills folder, e.g.
`~/.agents/skills/ctf-playbook/`.

## Usage

Once installed, ask your agent to use `ctf-playbook` when starting a CTF, or load the skill
explicitly. The playbook is written to be read by an AI agent and applied step by step.

```bash
python ctf-playbook/scripts/recon.py <TARGET>
python ctf-playbook/scripts/page_enum.py "http://<TARGET>:8081/page.php?id=" 1 10000
python ctf-playbook/scripts/prompt_inject.py "http://<TARGET>:8090" "<TOKEN>" "<BODY>"
python ctf-playbook/scripts/forge_jwt.py "<SECRET>" house-atriedes ducal-scribe decree:draft
python ctf-playbook/scripts/mavlink_signed.py <TARGET> "<KEY_HEX>" <LAT> <LON> <ALT>
```

## Structure

```
ctf-playbook/
├── SKILL.md                     the playbook (rules, patterns, recipes)
├── scripts/
│   ├── prompt_inject.py
│   ├── forge_jwt.py
│   ├── scan_page_ids.py
│   └── mavlink_signed.py
└── reference/
    └── ctf-usv-2026-dune.md     sanitized case study
```

## Philosophy

- A flag is behind an **intended vulnerability**, never behind a random 32-byte secret.
- If you are brute-forcing randomness, you are on the wrong path.
- When the model refuses, change the **framing**; when output is masked, ask for a **modified**
  value; when a page is a decoy, enumerate the whole range and diff.
- Retry LLM/template requests: they are probabilistic.

## Contributing

This playbook improves one competition at a time. After each CTF:

1. Append the new lessons to the **Changelog** at the end of `SKILL.md`.
2. Add reusable scripts under `scripts/`.
3. Add sanitized case studies under `reference/` (no real credentials, no live flags).

## License

MIT
