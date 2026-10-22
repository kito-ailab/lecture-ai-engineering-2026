"""第1回: LLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --chat     # 会話履歴を引き継いで質問を続ける
    uv run python -m app.ask --chat "LoRAとは何ですか？"

通常はツールも会話履歴も持たない「素の」呼び出し。--chat では実行中の会話を保持する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors
from google.genai.types import GenerateContentResponse

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_usage(response: GenerateContentResponse) -> None:
    """1回の応答に含まれる入力・出力トークン数を表示する。"""
    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else None
    output_tokens = usage.candidates_token_count if usage else None
    print(
        f"[トークン数] 入力: {input_tokens if input_tokens is not None else '不明'} / "
        f"出力: {output_tokens if output_tokens is not None else '不明'}"
    )


def ask(question: str) -> str:
    with genai.Client(api_key=get_api_key()) as client:
        response = client.models.generate_content(model=MODEL, contents=question)
    print_usage(response)
    return response.text


def chat(initial_question: str | None = None) -> None:
    """同じチャットを使い続け、ユーザーとモデルの両方の発言を引き継ぐ。"""
    print("対話モードです。/exit または /quit で終了します。")
    print("会話履歴はこの実行中だけ保持し、ファイルには保存しません。\n")
    try:
        with genai.Client(api_key=get_api_key()) as client:
            conversation = client.chats.create(model=MODEL)
            question = initial_question
            while True:
                if question is None:
                    question = input("あなた> ")
                else:
                    print(f"あなた> {question}")
                message = question.strip()
                question = None
                if message.lower() in {"/exit", "/quit"}:
                    break
                if not message:
                    continue
                try:
                    response = conversation.send_message(message)
                except errors.APIError as e:
                    print(api_error_message(e.code, e.message))
                    continue
                print_usage(response)
                print(f"AI> {response.text}\n")
    except (EOFError, KeyboardInterrupt):
        pass
    print("\n対話を終了しました。")


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--chat", action="store_true", help="会話履歴を引き継いで対話する")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    if args.chat:
        chat(args.question)
        return
    question = args.question if args.question is not None else DEFAULT_QUESTION
    print(f"[質問] {question}\n")
    try:
        print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
