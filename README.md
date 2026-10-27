<a href="https://coletebou.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img alt="Cole Tebou’s Almanac and Ephemeris for the Year of Our Lord 2026: agentic systems in production, enterprise AI for the nuclear industry, a platform of personal AI agents and the coding-agent fleet that builds it, with a star chart of Orion and the Pleiades, the phases of the Moon, and Psalm 19:1." src="assets/banner-light.svg" width="100%">
  </picture>
</a>

I build agentic systems and run them in production.

**In the enterprise,** I build AI and engineering systems for the advanced nuclear industry: agentic
workflows and platform capabilities on AWS, built for reliability, access control and traceable results.

**[Badland](https://badland.ai) is my own platform.** It gives each person an AI agent of their own, with
its own memory, skills, tools and scheduled jobs, that they text over iMessage and SMS. More than a hundred
are provisioned, each in its own container; idle agents sleep and wake on the next text, so one server
carries them all.

**A fleet of coding agents builds and runs it:** dozens of Claude Code and Codex sessions across my
machines that plan, build, review and deploy. They hand their work to fresh sessions in chains now more
than thirty generations deep, share one memory, and answer to a manager agent that keeps them moving.

Before software I was a structural engineer on heavy civil and industrial projects, from a $100M ship-lift
drydock to a $250M industrial plant. The stack that runs my fleet is open source:

## The agent stack

<table>
<tr>
<td width="50%" valign="top">

### [Drover](https://github.com/coletebou/drover)

**The control plane.** Every Claude Code session, Codex thread and Grok bot on every host, in three
lanes: waiting on you, working, idle. A manager agent reads the board and keeps the fleet moving. Answer, message and launch them from a browser, a terminal, a
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
