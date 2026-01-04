# プログレス管理アプリケーション

Pythonとtkinterで作成されたシンプルなプログレス管理アプリケーションです。

## 機能

- **5行のプログレス管理**: 5つの異なる項目を同時に管理できます
- **カスタマイズ可能**: 各行の項目名と最大値を自由に設定できます
- **＋/－ボタン**: ワンクリックで現在値を1ずつ増減できます
- **リアルタイム可視化**: 棒グラフで達成度を視覚的に確認できます
- **カラーコーディング**: 達成度に応じて色が変化します
  - 0-25%: 青
  - 25-50%: オレンジ
  - 50-75%: 黄色
  - 75-100%: 黄緑
  - 100%: 緑
- **パーセント表示**: 各プログレスバーに達成率が表示されます

## 必要要件

- Python 3.7以上
- tkinter（通常Pythonに標準搭載）

## インストール

### Pythonスクリプトとして実行する場合

```bash
# リポジトリをクローンまたはダウンロード
git clone <your-repository-url>
cd progress_bar_app

# 直接実行（tkinterは標準ライブラリなので追加インストール不要）
python progress_manager.py
```

### EXEファイルとして作成する場合

#### Windows

```bash
# PyInstallerをインストール
pip install -r requirements.txt

# EXE化スクリプトを実行
build_exe.bat
```

#### macOS/Linux

```bash
# PyInstallerをインストール
pip install -r requirements.txt

# 実行権限を付与
chmod +x build_exe.sh

# EXE化スクリプトを実行
./build_exe.sh
```

EXE化が完了すると、`dist`フォルダ内に実行ファイルが生成されます。

## 使用方法

### 基本的な使い方

1. **アプリケーションを起動**
   - Pythonスクリプト: `python progress_manager.py`
   - EXEファイル: `dist`フォルダ内の実行ファイルをダブルクリック

2. **項目の設定**
   - 各行の「項目名」フィールドに管理したい項目名を入力
   - 「最大値」フィールドに目標値を入力

3. **進捗の更新**
   - 「＋」ボタン: 現在値を1増やす
   - 「－」ボタン: 現在値を1減らす
   - 「リセット」ボタン: その行の現在値を0にリセット

4. **全体のリセット**
   - 画面下部の「全てリセット」ボタンで全行の現在値を0にリセット

### 使用例

#### タスク管理
- 項目名: "レポート作成"、最大値: 10（ページ数）
- 項目名: "コーディング"、最大値: 50（機能数）
- 項目名: "テスト"、最大値: 100（テストケース数）

#### 学習進捗管理
- 項目名: "数学の問題集"、最大値: 200（問題数）
- 項目名: "英単語暗記"、最大値: 500（単語数）
- 項目名: "プログラミング演習"、最大値: 30（演習数）

#### 習慣トラッキング
- 項目名: "筋トレ"、最大値: 30（日数）
- 項目名: "読書"、最大値: 365（ページ数）
- 項目名: "瞑想"、最大値: 100（セッション数）

## ファイル構成

```
progress_bar_app/
├── progress_manager.py    # メインアプリケーション
├── requirements.txt       # 依存パッケージ
├── build_exe.bat         # Windows用EXE化スクリプト
├── build_exe.sh          # macOS/Linux用EXE化スクリプト
└── README.md             # このファイル
```

## トラブルシューティング

### tkinterがインストールされていない場合

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Pythonの公式インストーラーを使用している場合、tkinterは自動的にインストールされます。

### EXE化で問題が発生する場合

```bash
# PyInstallerを再インストール
pip uninstall pyinstaller
pip install pyinstaller

# キャッシュをクリアして再ビルド
pyinstaller --clean --onefile --windowed --name "プログレス管理アプリ" progress_manager.py
```

## カスタマイズ

### 行数を変更する場合

`progress_manager.py`の`ProgressManagerApp`クラスの`__init__`メソッド内で、以下の部分を変更します：

```python
# 5行のプログレス行を作成
self.progress_rows = []
for i in range(5):  # ←この数値を変更
    row = ProgressRow(main_frame, i + 1)
    self.progress_rows.append(row)
```

### 色を変更する場合

`ProgressRow`クラスの`draw_progress_bar`メソッド内の色設定を変更します：

```python
if percentage >= 100:
    bar_color = '#4CAF50'  # 緑（完了）
elif percentage >= 75:
    bar_color = '#8BC34A'  # 黄緑
# ... など
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 作成日

2026-01-04

## バージョン

1.0.0

