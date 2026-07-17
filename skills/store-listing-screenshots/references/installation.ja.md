# インストール

`store-listing-screenshots`フォルダは、単体で動作するAgent Skillです。`SKILL.md`だけではなく、フォルダ全体をインストールしてください。

## Codex

次の場所へSkillフォルダ全体をインストールします。

```text
~/.agents/skills/store-listing-screenshots/
```

特定のプロジェクトだけで使う場合は、次の場所にも配置できます。

```text
<project>/.agents/skills/store-listing-screenshots/
```

`$store-listing-screenshots`と指定するか、ストア掲載画像を作りたいと依頼すると起動できます。

## Claude Code

同じSkillフォルダを次の場所へインストールします。

```text
~/.claude/skills/store-listing-screenshots/
```

特定のプロジェクトだけで使う場合は、次の場所にも配置できます。

```text
<project>/.claude/skills/store-listing-screenshots/
```

`/store-listing-screenshots`と指定するか、ストア掲載画像を作りたいと依頼すると起動できます。

## ほかのAgent Skills対応ツール

各ツールが指定するSkill保存先へフォルダ全体をインストールしてください。`SKILL.md`、`scripts`、`assets`、`references`、`requirements.txt`を同じフォルダ内に保つ必要があります。

`agents/openai.yaml`はCodex向けの表示設定です。Claude Codeなど、ほかのツールでは無視されても動作に影響しません。
