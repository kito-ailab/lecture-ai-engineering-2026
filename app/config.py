"""講座全体で共通の設定。

APIキーやモデル名は、環境変数またはプロジェクト直下の .env から読み込む。
"""

import os
from pathlib import Path

from dotenv import dotenv_values

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def _get_setting(name: str, default: str | None = None) -> str | None:
    # 親ディレクトリや作業ディレクトリの .env は探索しない。
    # os.environ に追加せず、MCP などの子プロセスへキーを自動で渡さない。
    if name in os.environ:
        return os.environ[name]
    return dotenv_values(ENV_FILE, encoding="utf-8", interpolate=False).get(name, default)


# 既定モデル。環境変数 AIE_MODEL を設定すると切り替えられる。
#   例: export AIE_MODEL=gemini-3.5-flash
DEFAULT_MODEL = "gemini-3.5-flash-lite"
MODEL = _get_setting("AIE_MODEL", DEFAULT_MODEL) or DEFAULT_MODEL


def api_error_message(status: int, detail: str = "") -> str:
    """HTTPステータスコードを、受講生向けの日本語の説明にする（ask.py と agent.py で共用）。"""
    if status == 429:
        return "レート制限に達しました。1分ほど待ってから再実行してください。"
    if status == 503:
        return "モデルが混み合っています（503）。少し待ってから再実行してください。"
    if status in (400, 401, 403, 404):
        return f"APIキーかモデル名に問題があります（{status}）: {detail}"
    return f"APIエラー（{status}）: {detail}"


def get_api_key() -> str:
    """環境変数を優先してAPIキーを読み、未設定なら値を表示せずに終了する。"""
    key = (_get_setting("GEMINI_API_KEY") or "").strip()
    if not key:
        raise SystemExit(
            "GEMINI_API_KEY が未設定または空です。\n"
            "ローカルの VS Code: プロジェクト直下に .env を作成し、\n"
            "GEMINI_API_KEY に取得済みのキーを設定してください。\n"
            "環境変数が設定済みの場合は、.env より優先されます。\n"
            "Codespaces: secret に GEMINI_API_KEY を登録し、再起動してください。\n"
            "キーをコード・コミット・チャットに貼らないでください。"
        )
    return key
