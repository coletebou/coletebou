<a href="https://coletebou.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img alt="Cole Tebou: software engineer, tools for running fleets of coding agents. An engineering cover sheet: a utility plan ties Claude Code, Codex, Grok bots and OpenClaw into the Drover control plane, above the badland-brain shared memory and the dx environment." src="assets/banner-light.svg" width="100%">
  </picture>
</a>

I build the tooling for running a fleet of coding agents: a control plane that sees every Claude Code
and Codex session on every machine, one memory they all share, and the environment underneath them.
On top of it I run [Badland](https://badland.ai): a personal AI agent you text over iMessage, SMS and
Telegram, and a chat app that puts three AIs on one prompt, side by side.

## The fleet

<table>
<tr>
<td width="50%" valign="top">

### [Drover](https://github.com/coletebou/drover)

**The control plane.** Every Claude Code session, Codex thread and Grok bot on every host, in three
lanes: waiting on you, working, idle. Answer, message and launch them from a browser, a terminal, a
Mac, an iPhone, a watch or a browser extension. One daemon per machine, zero npm dependencies, no open
ports.

`Node 24` `Swift` `MCP` `tmux`

</td>
<td width="50%" valign="top">

### [badland-brain](https://github.com/coletebou/badland-brain)

**The shared memory.** One self-hosted memory for Claude Code, Codex, ChatGPT and any MCP client.
Hybrid keyword and vector search, facts that keep their history, per-agent keys, a write gate that
refuses secrets, and provenance on everything an agent reads back.

`TypeScript` `MCP` `SQLite FTS5 + sqlite-vec` `MongoDB`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### dx <sub>opening soon</sub>

**The environment.** Dotfiles for running fleets of coding agents: Claude Code and Codex hooks, a
skills marketplace, tmux, git worktrees, session handoff chains and agent memory. macOS and Linux.

`zsh` `tmux` `Claude Code` `Codex`

</td>
<td width="50%" valign="top">

### [porchlight](https://github.com/coletebou/porchlight)

**The login screen.** A fleet-aware MOTD: vitals, services, AI agents and their plan limits,
containers, pull requests and cloud status, ranked into one attention list and rendered from cache in
milliseconds.

`Python 3.9+` `zero dependencies`

</td>
</tr>
</table>

## Also on the drafting table

| | |
|---|---|
| **[Badland Line](https://github.com/Badland-AI/grokbot)** | Text your Grok Bot from any phone over SMS: a remote MCP server and a skill. |
| **[grok-bot-backup](https://github.com/coletebou/grok-bot-backup)** | Back up every Grok Bot, routine and skill to git as plain files. Unofficial and read-only. |
| **[Tide](https://github.com/coletebou/tide)** | A native code editor for iPad and iPhone in the spirit of VS Code, in Swift. Early. |
| **[Airspace Lab](https://github.com/coletebou/airspace-lab)** | Orbit, slice and probe U.S. terminal airspace in 3D instead of memorizing a sectional. |
| **[Excito](https://github.com/coletebou/Excito)** | Earthquake ground-motion spectral matching: legacy Fortran behind a Python command line. |

## Upstream

Pull requests merged into other people's projects, as of October 2026: 72 to
[ooxml](https://github.com/ChristopherVR/ooxml) (the logic behind its Office viewers) and 10 across
[OpenClaw](https://github.com/openclaw)'s projects: 8 to [Clawpatch](https://github.com/openclaw/clawpatch),
and one each to [OpenClaw](https://github.com/openclaw/openclaw) itself and [imsg](https://github.com/openclaw/imsg).
Five more are open on OpenClaw.
[Every merged pull request](https://github.com/search?q=author%3Acoletebou+is%3Apr+is%3Amerged+-user%3Acoletebou+-org%3ABadland-AI&type=pullrequests).

---

<p>
  <a href="https://coletebou.com">coletebou.com</a> ·
  <a href="https://plans.coletebou.com">the plan set</a> ·
  <a href="https://coletebou.github.io">coletebou.github.io</a> ·
  <a href="https://badland.ai">badland.ai</a> ·
  <a href="https://www.linkedin.com/in/cole-tebou">LinkedIn</a> ·
  <a href="https://x.com/coletebou">X</a>
</p>
<!-- When the terminal edition ships, add: <a href="https://term.coletebou.com">the terminal</a> -->
