# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：`glossary_search_glossary`、`glossary_get_lecture_summary`
- STEP 2 の [tool call]：`[tool call]   glossary_search_glossary({'query': '3レベル'})`
- STEP 3 の [tool call]：`[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})`
- STEP 4 の [tool call]：
  ```text
  [tool call]   aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニングとは'})
  [tool call]   aws_aws___search_documentation({'search_phrase': 'what is Amazon S3 versioning'})
  ```
- 気づき・疑問：MCPのツール名には、設定したサーバー名が接頭辞として付く。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：`app/mcp_server.py` で `get_lecture_summary` を公開した。
- 結果：エージェントに渡されるツール一覧に `glossary_get_lecture_summary` が追加された。「第2回では何を学びますか？」と質問したところ、Geminiが以下のツールを選び、第2回の要点を受け取って回答した。モデル応答は2回だった。ローカルのテストモデルでもMCP経由で要点が返ることを確認し、テストは18件すべて通過した。

  ```text
  [tool call] glossary_get_lecture_summary({'lecture': 2})
  ```

- 気づき・疑問：サーバー側でツールを公開すると、エージェント側で関数を直接登録しなくても、サーバーから取得した一覧に追加される。
