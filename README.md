<a href="https://coletebou.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img alt="Cole Tebou’s Almanac and Ephemeris for the Year of Our Lord 2026: a software engineer building tools for running fleets of coding agents (the Drover control plane, the badland-brain shared memory and the dx environment), with a star chart of Orion and the Pleiades, the phases of the Moon, and Psalm 19:1." src="assets/banner-light.svg" width="100%">
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

### [dx](https://github.com/coletebou/dx)

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

## Sites

| | |
|---|---|
| **[agent.badland.ai](https://agent.badland.ai)** | Your own AI agent in iMessage and SMS. No new app: sign up and it texts you. |
| **[tallgrass.social](https://tallgrass.social)** | Go find something wild: identify what you find, keep your discoveries, explore with friends. |
| **[starheart.ai](https://starheart.ai)** | Intelligence in service of the Creator: AI used to glorify God, a light in a dark world. |
| **[sunnydayz.co](https://sunnydayz.co)** | Family outdoor gear for trading screen time for sunshine. |
| **[chat.badland.ai](https://chat.badland.ai)** | Three AIs answer one prompt side by side, with image generation and voice. |
| **[coletebou.com](https://coletebou.com)** | My portfolio, the almanac edition. |
| **[plans.coletebou.com](https://plans.coletebou.com)** | The same portfolio, drawn as a set of engineering sheets. |
| **[term.coletebou.com](https://term.coletebou.com)** | And as a shell: `ls` the works, open one. |
| **[coletebou.github.io](https://coletebou.github.io)** | The index of all three editions. |
| **[badland.ai](https://badland.ai)** | Badland: AI built for independence. |
| **[arena.badland.ai](https://arena.badland.ai)** | ROOTFALL: a 3D AI battle royale you can watch live. |
| **[nebulatio.com](https://nebulatio.com)** | Nebulatio Studio: web design and development. |

## Upstream

Pull requests merged into other people's projects, as of October 2026: 72 to
[ooxml](https://github.com/ChristopherVR/ooxml) (the logic behind its Office viewers) and 10 across
[OpenClaw](https://github.com/openclaw)'s projects: 8 to [Clawpatch](https://github.com/openclaw/clawpatch),
and one each to [OpenClaw](https://github.com/openclaw/openclaw) itself and [imsg](https://github.com/openclaw/imsg).
Five more are open on OpenClaw.
[Every merged pull request](https://github.com/search?q=author%3Acoletebou+is%3Apr+is%3Amerged+-user%3Acoletebou+-org%3ABadland-AI&type=pullrequests).

---

<p>
  <a href="https://www.linkedin.com/in/cole-tebou">LinkedIn</a> ·
  <a href="https://x.com/coletebou">X</a>
</p>
