# Garmin MCP Server (Read-Only Fork)

> Fork of [Taxuspt/garmin_mcp](https://github.com/Taxuspt/garmin_mcp) — **全ての書き込みツールを削除**し、LLMのプロンプトインジェクションによるGarmin Connectデータの意図しない改ざんを防止した読み取り専用バージョンです。

Garmin's API is accessed via [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) library.

## Read-Only化の変更点

### セキュリティ対策

- **書き込みツール16個を全削除**: upload, delete, create, update, log, set 系のツールをLLMから一切呼び出せないようにしました
- **mcp SDKバージョンを固定**: `>=1.23.0,<2.0.0`（CVE-2025-53365対策済みバージョン）
- **Renovate設定追加**: 依存関係のセキュリティアップデートを自動化

### 有効なツール（52個・全て読み取り専用）

| モジュール | ツール数 | 内容 |
|---|---|---|
| Activity Management | 13 | アクティビティ一覧、詳細、スプリット、天気、心拍ゾーン等 |
| Health & Wellness | 25 | 歩数、心拍、睡眠、ストレス、呼吸、Body Battery、トレーニングレディネス等 |
| Training & Performance | 8 | HRV、乳酸閾値、持久力スコア、トレーニングステータス等 |
| Workouts | 5 | ワークアウト一覧、詳細、スケジュール、トレーニングプラン |
| Gear Management | 1 | ギア一覧・使用統計 |

### 無効化したモジュール・ツール

- **書き込みツール（削除）**: `upload_workout`, `delete_workout`, `schedule_workout`, `add_weigh_in`, `delete_weigh_ins`, `add_body_composition`, `set_blood_pressure`, `add_hydration_data`, `create_custom_food`, `update_custom_food`, `log_food`, `add_gear_to_activity`, `remove_gear_from_activity`, `request_reload` 等
- **未使用モジュール（無効化）**: User Profile, Devices, Weight Management, Challenges & Badges, Nutrition, Women's Health, Data Management

## セットアップ

### 前提条件

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- Garmin Connect アカウント

### Step 1: リポジトリのクローンと依存関係のインストール

```bash
git clone https://github.com/faruryo/garmin_mcp.git
cd garmin_mcp
uv sync
```

### Step 2: 事前認証（初回のみ）

```bash
uv run garmin-mcp-auth
```

メール・パスワード・MFAコードを入力すると、OAuthトークンが `~/.garminconnect` に保存されます。

トークンの検証:
```bash
uv run garmin-mcp-auth --verify
```

トークンが期限切れの場合:
```bash
uv run garmin-mcp-auth --force-reauth
```

### Step 3: Claude Desktopに設定

`~/Library/Application Support/Claude/claude_desktop_config.json` に追加:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/garmin_mcp",
        "run",
        "garmin-mcp"
      ],
      "env": {
        "GARMINTOKENS": "~/.garminconnect"
      }
    }
  }
}
```

`/path/to/garmin_mcp` はクローンしたディレクトリの絶対パスに置き換えてください。設定ファイルにパスワードは不要です。

### Claude Codeの場合

プロジェクトスコープで追加:
```bash
claude mcp add -s local \
  -e "GARMINTOKENS=$HOME/.garminconnect" \
  -- garmin uv --directory /path/to/garmin_mcp run garmin-mcp
```

`/path/to/garmin_mcp` はクローンしたディレクトリの絶対パスに置き換えてください。

### Step 4: Claude Desktopを再起動

動作確認:
```
Garminから今日の歩数とステータスを教えて
```

## MCP Inspectorでのテスト

```bash
npx @modelcontextprotocol/inspector uv run garmin-mcp
```

## テスト

```bash
# 有効なモジュールのインテグレーションテスト
uv run pytest tests/integration/ -v

# E2Eテスト（実際のGarmin認証情報が必要）
uv run pytest tests/e2e/ -m e2e -v
```

## Upstream

本フォークは [Taxuspt/garmin_mcp](https://github.com/Taxuspt/garmin_mcp) をベースにしています。上流の全機能（書き込みツール含む）については上流リポジトリを参照してください。
