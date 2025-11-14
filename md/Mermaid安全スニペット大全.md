# Mermaid安全スニペット大全（14種・直接ラベル版）
*注：IDは英字開始＋ASCII英数/アンダースコア。ラベルは**具体的日本語**。禁止記号は使用しないこと。*

## 1. flowchart
```mermaid
flowchart TD
    fc_start[準備の確認] --> fc_plan[方針を決める]
    fc_plan -->|条件A| fc_pathA[方法Aで実行]
    fc_plan -->|条件B| fc_pathB[方法Bで実行]
    fc_pathA --> fc_check[結果を点検]
    fc_pathB --> fc_check[結果を点検]
    fc_check -->|合格| fc_done[完了]
    fc_check -->|不合格| fc_fix[修正して再実行]
```

## 2. sequenceDiagram
```mermaid
sequenceDiagram
    participant sq_user as 利用者
    participant sq_sys as 仕組み
    sq_user->>sq_sys: 依頼を送る
    sq_sys-->>sq_user: 結果を返す
```

## 3. stateDiagram-v2
```mermaid
stateDiagram-v2
    [*] --> st_準備
    st_準備 --> st_実行: 条件成立
    st_実行 --> st_確認: 完了
    st_確認 --> [*]: 合格
    st_確認 --> st_実行: 不合格→再実行
```

## 4. classDiagram
```mermaid
classDiagram
    class cl_帳票 {
        生成日
        作成者
        出力()
    }
    class cl_承認者 {
        氏名
        承認()
    }
    cl_承認者 --> cl_帳票 : 確認する
```

## 5. erDiagram
```mermaid
erDiagram
    ER_顧客 ||--o{ ER_注文 : もつ
    ER_注文 }o--|| ER_商品 : ふくむ
```

## 6. gantt
```mermaid
gantt
    title スケジュール
    dateFormat  YYYY-MM-DD
    section 準備
    企画:done, gg_企画, 2025-01-10, 3d
    設計:gg_設計, 2025-01-15, 4d
    section 実行
    実装:gg_実装, 2025-01-20, 5d
```

## 7. timeline
```mermaid
timeline
    title 進行の流れ
    事前: 準備
    実行: 作業/検証
    事後: 共有/改善
```

## 8. journey
```mermaid
journey
    title 体験の流れ
    section 準備
      手順を確認: 3: 利用者
    section 実行
      操作を行う: 2: 利用者
    section 結果
      振り返る: 4: 利用者
```

## 9. quadrantChart
```mermaid
quadrantChart
    title 優先度マップ
    x-axis 影響が小さい --> 影響が大きい
    y-axis 実行が難しい --> 実行が易しい
    qd_改善A: [1, 4]
    qd_改善B: [3, 2]
```

## 10. pie
```mermaid
pie showData
    title 構成の割合
    "項目A" : 40
    "項目B" : 35
    "項目C" : 25
```

## 11. gitGraph
```mermaid
gitGraph
    commit id: "gg_開始"
    branch gg_作業
    checkout gg_作業
    commit id: "gg_変更1"
    checkout main
    merge gg_作業
```

## 12. mindmap
```mermaid
mindmap
  root((テーマ))
    目的
      指標
    手段
      図解
      物語
```

## 13. requirementDiagram
```mermaid
requirementDiagram
    requirement rq_要件A {
      説明: 目的を明確にする
      合否: 観察で確認
    }
    requirement rq_要件B {
      説明: 手順が再現できる
      合否: 実演で確認
    }
```

## 14. C4Context
```mermaid
C4Context
    title 仕組みの全体像
    Person(p_利用者, "利用者", "使う人")
    System(s_サービス, "サービス", "提供する機能")
    Person_Ext(p_管理者, "管理者", "支える人")
    Rel(p_利用者, s_サービス, "依頼する")
    Rel(p_管理者, s_サービス, "運用する")
```