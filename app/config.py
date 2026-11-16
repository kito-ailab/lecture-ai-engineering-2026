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

# 第5回: 1ページを1チャンクとして検索する。索引はscripts/build_rag_index.pyで作成する。
ROOT = Path(__file__).resolve().parent.parent
RAG_SOURCE = ROOT / "data/rag_data/lectures.json"
RAG_TREE = ROOT / "data/rag_data/tree.json"
RAG_GRAPH = ROOT / "data/rag_data/graph.json"
RAG_DB = Path(os.getenv("AIE_RAG_DB", str(ROOT / "data/rag_data/index.sqlite3")))
RAG_DOCUMENT_IDS = ("lec01-main", "lec02-main", "lec03-main")
RAG_TOP_K = 5
GRAPH_START_K = 3
GRAPH_HOPS = 2
GRAPH_MAX_RESULTS = 10
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768
# 2,048トークンの上限に対し、タスク指定等の分を残す。超過時は切り捨てず停止する。
EMBEDDING_MAX_TOKENS = 2000


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
