# pyproject.toml を書くための知識体系（Module 08 / ex1 向け）

`loading.py` の依存を Poetry で宣言するために必要な知識を、下の層から順に積み上げる形でまとめる。

- 第1層：TOML という「入れ物」の文法
- 第2層：pyproject.toml が何のためのファイルか（標準としての位置づけ）
- 第3層：Poetry が使うセクション構造
- 第4層：依存とバージョン制約の記法
- 第5層：requirements.txt との対応と、ex1 での最小完成形

---

## 第1層：TOML の文法（入れ物のルール）

pyproject.toml は **TOML** という設定記述フォーマットで書く。TOML は「人間が読み書きしやすい設定ファイル」を狙った形式で、INI に近いが型を持つ。最低限これだけ押さえれば読める。

### キーと値

```toml
name = "loading"      # 文字列はダブルクォート
version = "0.1.0"
```

- `キー = 値` の形。`=` の両側にスペースを入れるのが慣習。
- 文字列は `"..."`。数値・真偽値はクォート不要（`123`, `true`）。

### テーブル（セクション）

`[...]` で「テーブル」を作る。中括弧のセクション見出しのようなもの。

```toml
[tool.poetry]
name = "loading"
```

- `[tool.poetry]` は「`tool` の中の `poetry`」という**入れ子**を表す。ドットが階層の区切り。
- 見出しを書いた次の行から、次の `[...]` が来るまでが、そのテーブルの中身。

### 配列

```toml
authors = ["Takaho"]
keywords = ["data", "matrix"]
```

- 角括弧 `[...]` で並べる。カンマ区切り。

### 覚えておく落とし穴

- **順序に依存しない**が、テーブル見出しの下に書いた行はそのテーブルに属する。どのテーブルの下にいるかを常に意識する。
- インデントは意味を持たない（YAML と違う）。見やすさのために揃えるのは自由。
- コメントは `#`。

---

## 第2層：pyproject.toml とは何か

### 標準ファイルとしての位置づけ

`pyproject.toml` は特定ツール専用ではなく、**Python プロジェクトの設定を1か所に集約するための標準ファイル**（PEP 518 で導入）。もともとは「このプロジェクトをビルドするのに何が要るか」を書く場所として生まれ、そこから依存管理・各種ツール設定まで載せるハブに育った。

ここに載りうるもの：

- プロジェクトのメタ情報（名前・バージョン・作者）
- 依存パッケージの宣言
- ビルドシステムの指定
- flake8 / mypy / black などツールの設定（`[tool.*]` 配下）

### requirements.txt との思想差（再確認）

| | requirements.txt | pyproject.toml |
|---|---|---|
| 形式 | 平テキスト（1行1パッケージ） | 構造化 TOML |
| 表現するもの | 「入れるものリスト（買い物リスト）」 | 「プロジェクトの要求仕様＋メタ情報」 |
| Python 自体の版指定 | 不可 | 可 |
| 依存以外の設定 | 書けない | ツール設定も同居できる |
| 対応ツール | pip | Poetry / uv / pip(PEP 621) など |

**要点**：requirements.txt が「何を入れるか」だけを持つのに対し、pyproject.toml は「このプロジェクトはどういうものか」を宣言するファイル。依存はその一部にすぎない。

---

## 第3層：Poetry が使うセクション構造

Poetry で書く場合、pyproject.toml は主に3つのテーブルで構成される。

### 1. メタ情報をどこに書くか — 旧形式と標準形式のねじれ

ここには**重要な設計上の注意**がある。`name` / `version` / `description` / `authors` は本来「**プロジェクト（成果物）のメタデータ**」であって、「Poetry というツールの設定」ではない。ところが古い Poetry ではこれを `[tool.poetry]` の下に書いていた。

```toml
[tool.poetry]        # ← 旧形式。メタ情報がツールセクションに同居している
name = "loading"
version = "0.1.0"
description = "Matrix data analysis tool"
authors = ["Takaho"]
```

**なぜツールセクションにプロジェクトのメタ情報があるのか（歴史的経緯）**：

1. Poetry が独自にこの形式を作った時点（2018年頃）、依存やメタ情報を書く**標準がまだ存在しなかった**。
2. `[tool.*]` は PEP 518 が「各ツールが自由に使ってよい名前空間」として用意した区画。Poetry はそこに自分用の設定として、メタ情報も依存も全部詰め込んだ。
3. **後から** PEP 621 で「プロジェクトのメタ情報はツール非依存の標準セクション `[project]` に書くべき」という合意ができた。

つまり `[tool.poetry]` にメタ情報があるのは「Poetry が標準より先に生まれてしまった」という**順序の産物**であり、意味論的には綺麗ではない。`[tool.*]` の本来の趣旨は「そのツールをどう動かすか」の設定を置く区画なので、`name` や `authors` のような「プロジェクトが何か」を表す情報はミスマッチ。

**標準形式（PEP 621）による解消**：メタ情報は標準の `[project]` へ、Poetry 固有の設定だけ `[tool.poetry]` へ、と役割で分離する。

```toml
[project]            # ← プロジェクトのメタ情報（ツール非依存の標準）
name = "loading"
version = "0.1.0"
description = "Matrix data analysis tool"
authors = [{ name = "Takaho" }]
requires-python = ">=3.10"

[tool.poetry]        # ← ここには Poetry 固有の設定だけが残る
package-mode = false
```

他言語ではこの分離が最初から自然で、Ruby の gemspec は gem のメタ情報専用ファイルだし、Node の package.json も `name`/`version` はトップレベルにあってツール設定ではない。Python は標準化が後追いだったため、この過渡期のねじれが残った。

**どちらを使うか**：
- 旧形式（`[tool.poetry]` にメタ情報）… 古い教材・既存プロジェクトで今も多数見る。Poetry 1.x 系の標準。「レガシーだが現役」。
- 標準形式（`[project]` に分離）… 意味論的に正しく標準準拠。Poetry 2.0+ 前提。

**peer-review 的には**、「メタ情報はツール非依存であるべきだから `[project]` に置いた」と説明できると理解の深さを示せる。ただし標準形式では依存のバージョン記法が pip 風になる（第4層・第5層参照）点と、手元の Poetry が 2.0 以上かの確認が要る点に注意。環境が古いと旧形式しか動かない。

補助オプション：`package-mode = false` を `[tool.poetry]` に足すと「配布用パッケージではなくアプリ」として扱われ、name/version の制約が緩くなる（ex1 のような単発スクリプトで楽になる場合がある）。

### 2. `[tool.poetry.dependencies]` — 依存（旧形式の場合）

**直接依存だけ**を並べる。間接依存（pandas が連れてくる pytz など）は書かない ── Poetry が依存解決で自動的に見つけて lock に記録する。

```toml
[tool.poetry.dependencies]
python = "^3.10"
numpy = "^1.26.0"
pandas = "^2.1.0"
matplotlib = "^3.8.0"
```

- 先頭の `python = "^3.10"` は**Python インタプリタ自体の版要求**。requirements.txt には無い概念で、pyproject.toml ならではの表現。
- 各行が「このプロジェクトが直接使うパッケージ」。バージョン記法は第4層で詳述。

### 3. `[build-system]` — ビルド方法の宣言

「このプロジェクトをどのツールで組み立てるか」を宣言する。Poetry を使う印。

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry-core.masonry.api"
```

- ex1 のような実行スクリプトでは意識する場面は少ないが、Poetry が正しく動くために存在する定型ブロック。`poetry init` が自動生成する。

---

## 第4層：バージョン制約の記法

ここが pip と最も紛らわしい部分。Poetry 独自の `^` と `~` の意味を正確に。

### 前提：SemVer（セマンティックバージョニング）

`MAJOR.MINOR.PATCH`（例 `2.1.4`）という3数字の約束。

- MAJOR：後方互換を壊す変更（上げると壊れうる）
- MINOR：後方互換を保った機能追加
- PATCH：後方互換を保ったバグ修正

Poetry の `^` はこの約束を前提に「壊れない範囲で更新を許す」という発想で作られている。

### Poetry の記法

| 記法 | 意味 | 展開 |
|---|---|---|
| `^2.1.0` | メジャーを上げない（SemVer 互換の範囲） | `>=2.1.0,<3.0.0` |
| `~2.1.0` | マイナーを上げない | `>=2.1.0,<2.2.0` |
| `>=2.1,<3.0` | 明示的な範囲（カンマは AND） | そのまま |
| `2.1.4` | 完全固定 | ちょうどその版のみ |
| `*` | 何でも | 最新 |

`^`（キャレット）が Poetry のデフォルト思想。「メジャーが同じなら互換のはずだから、マイナー・パッチの更新は受け入れる。破壊的変更のあるメジャーだけ上げない」= `^2.1.0` は実質「2 系ならどれでも」。

### pip との対応（混乱ポイント）

同じ記号でも指す範囲が違う：

- pip の `~=1.26.0` = マイナー固定（`>=1.26.0,<1.27.0`）
- Poetry の `~1.26.0` = マイナー固定（同じ意味）
- Poetry の `^1.26.0` = メジャー固定（`>=1.26.0,<2.0.0`）← pip には対応する1文字記法が無く、範囲で明示する

**両ファイルを書くときの注意**：pyproject.toml で `^` を使ったら、requirements.txt では対応する範囲を `>=X,<X+1` の形で明示的に書く必要がある。記号を機械的にコピーしない。

---

## 第5層：requirements.txt との対応と ex1 の最小完成形

### 同じ意図を両形式で（対応表）

意図：numpy は 1.26 系、pandas は 2 系、matplotlib は 3.8 系以上を許す。

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.10"
numpy = "~1.26.0"      # マイナー固定
pandas = "^2.1.0"      # メジャー固定（2系）
matplotlib = "^3.8.0"  # メジャー固定（3系）
```

```
# requirements.txt（pip・同じ意図を明示範囲で）
numpy>=1.26.0,<1.27.0
pandas>=2.1.0,<3.0.0
matplotlib>=3.8.0,<4.0.0
```

再現性を最優先するなら requirements.txt 側は完全固定でもよい：

```
numpy==1.26.2
pandas==2.1.4
matplotlib==3.8.2
```

### pyproject.toml の最小完成形（Poetry）

```toml
[tool.poetry]
name = "loading"
version = "0.1.0"
description = "Matrix data analysis tool"
authors = ["Takaho"]

[tool.poetry.dependencies]
python = "^3.10"
numpy = "^1.26.0"
pandas = "^2.1.0"
matplotlib = "^3.8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry-core.masonry.api"
```

`requests` は API を叩く実装にした場合のみ足す（ex1 では任意）：

```toml
requests = "^2.31.0"
```

### 生成の実務

手書きよりも、対話生成 → 依存追加が楽：

```
poetry init          # 質問形式でメタ情報＋骨組みを生成
poetry add numpy pandas matplotlib   # 依存を足す（自動で解決・記録）
```

`poetry add` は pyproject.toml に追記しつつ、依存解決を走らせて poetry.lock も更新する。手書きした場合は `poetry install` で解決・インストールする。

---

## peer-review で説明できるべき論点（このファイルの要旨）

- pyproject.toml は「入れるものリスト」ではなく「プロジェクトの要求仕様」を宣言するファイル。
- `name`/`version`/`authors` は本来プロジェクトのメタ情報であり、標準では `[project]` に置くのが正しい。`[tool.poetry]` に入っているのは Poetry が標準（PEP 621）より先に生まれた名残。`[tool.*]` の本来の趣旨は「ツールをどう動かすか」の設定。
- 依存として書くのは**直接依存だけ**。間接依存は Poetry が解決して lock に記録する。
- `^` はメジャー固定、`~` はマイナー固定。pip の同名記法とは範囲が違う。
- pyproject.toml は範囲（人間の意図）を持ち、poetry.lock が確定版（再現用）を持つ、という役割分担で「開発しやすさ」と「再現性」を両立させる。
- requirements.txt（pip）と pyproject.toml（Poetry）は同じ依存集合を別の語彙で表したもので、記法の思想が違う。

---

## 補足：標準形式（PEP 621）の依存記法

第3層で触れた通り、メタ情報を `[project]` に分離する PEP 621 形式では、依存も `[project]` の `dependencies` に書く。この形式では `^`/`~` は使えず、**pip 風の範囲記法**になる点に注意。

```toml
[project]
name = "loading"
version = "0.1.0"
description = "Matrix data analysis tool"
authors = [{ name = "Takaho" }]
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.26.0,<2.0.0",
    "pandas>=2.1.0,<3.0.0",
    "matplotlib>=3.8.0,<4.0.0",
]

[tool.poetry]
package-mode = false

[build-system]
requires = ["poetry-core>=2.0"]
build-backend = "poetry.core.masonry.api"
```

- メタ情報・依存が `[project]`（標準）に集約され、`[tool.poetry]` には Poetry 固有設定だけが残る綺麗な分離になる。
- Poetry 2.0+ が前提。`requires-python` は旧形式の `python = "^3.10"` に対応する標準キー。
- `^`/`~` が使えないぶん、範囲は `>=X,<Y` で明示する。requirements.txt と記法が揃うので、両ファイルの対応は取りやすくなる。

**旧形式と標準形式のどちらか一方に絞る**のが、記法混在による混乱を避けるコツ。理解を示すなら標準形式、既存資産・古い環境に合わせるなら旧形式。