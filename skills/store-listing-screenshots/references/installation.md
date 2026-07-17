# Installation

The `store-listing-screenshots` directory is a self-contained Agent Skill. Install the whole directory, not only `SKILL.md`.

## Codex

Install or copy the directory to:

```text
~/.agents/skills/store-listing-screenshots/
```

Codex can also discover a project-scoped copy at:

```text
<project>/.agents/skills/store-listing-screenshots/
```

Invoke it explicitly with `$store-listing-screenshots`, or describe a matching store screenshot task.

## Claude Code

Install or copy the same directory to:

```text
~/.claude/skills/store-listing-screenshots/
```

Claude Code can also discover a project-scoped copy at:

```text
<project>/.claude/skills/store-listing-screenshots/
```

Invoke it explicitly with `/store-listing-screenshots`, or describe a matching store screenshot task.

## Other Agent Skills clients

Install the directory in the location required by that client. `SKILL.md`, `scripts`, `assets`, `references`, and `requirements.txt` must remain together.

`agents/openai.yaml` provides optional Codex presentation metadata. Other clients may ignore it safely.
