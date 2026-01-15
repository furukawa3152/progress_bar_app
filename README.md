# 業務進捗管理アプリケーション

Pythonとtkinterで作成されたシンプルな業務進捗管理アプリケーションです。

## 機能

- **6行のプログレス管理**: 6つの異なる業務を同時に管理できます
- **カスタマイズ可能**: 各行の業務内容と件数を自由に設定できます
- **＋/－ボタン**: ワンクリックで現在値を1ずつ増減できます
- **完了ボタン**: ワンクリックで現在値を件数の最大値に設定して100%にできます
- **コメント欄**: 各業務にコメントを追加できます
- **右上サマリー表示**: 入力済み項目を「業務内容：件数　コメント」形式でコピペ可能な形で表示
- **リアルタイム可視化**: 棒グラフで達成度を視覚的に確認できます
- **カラーコーディング**: 達成度に応じて色が変化します
  - 0-25%: 青
  - 25-50%: オレンジ
  - 50-75%: 黄色
  - 75-100%: 黄緑
  - 100%: 緑
- **パーセント表示**: 各プログレスバーに達成率が表示されます
- **自動保存**: データはCSVファイルに自動保存されます

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

または直接PyInstallerを実行：

```bash
python -m PyInstaller --onefile --windowed --name "業務進捗管理アプリ" progress_manager.py
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

2. **業務の設定**
   - 各行の「業務内容」フィールドに管理したい業務名を入力
   - 「件数」フィールドに目標件数を入力（デフォルト: 10）
   - 必要に応じて「コメント」欄にメモを入力

3. **進捗の更新**
   - 「＋」ボタン: 現在値を1増やす
   - 「－」ボタン: 現在値を1減らす
   - 「完了」ボタン: 現在値を件数の最大値に設定して100%にする
   - 「リセット」ボタン: 業務内容、件数、現在値、コメントをすべてリセット

4. **全体のリセット**
   - 画面下部の「全てリセット」ボタンで全行をリセット

5. **サマリー表示**
   - 画面右上の小窓に、入力済み項目（現在値が0より大きい、またはコメントがある項目）が表示されます
   - 「業務内容：件数　コメント」形式で表示され、コピペ可能です

### 使用例

#### 業務管理
- 業務内容: "レポート作成"、件数: 10（ページ数）
- 業務内容: "コーディング"、件数: 50（機能数）
- 業務内容: "テスト"、件数: 100（テストケース数）

#### タスク管理
- 業務内容: "メール返信"、件数: 20（件数）
- 業務内容: "会議資料作成"、件数: 5（資料数）
- 業務内容: "データ分析"、件数: 30（分析項目数）

## ファイル構成

```
progress_bar_app/
├── progress_manager.py    # メインアプリケーション
├── requirements.txt       # 依存パッケージ
├── build_exe.bat         # Windows用EXE化スクリプト
├── build_exe.sh          # macOS/Linux用EXE化スクリプト
├── progress_data.csv     # 進捗データ（自動生成）
└── README.md             # このファイル
```

## データ保存

- 進捗データは`progress_data.csv`に自動保存されます
- アプリケーションを再起動すると、前回のデータが自動的に読み込まれます
- CSVファイルには以下の情報が保存されます：
  - 行番号
  - 業務内容
  - 件数（最大値）
  - 現在値
  - コメント

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
python -m PyInstaller --clean --onefile --windowed --name "業務進捗管理アプリ" progress_manager.py
```

## カスタマイズ

### 行数を変更する場合

`progress_manager.py`の`ProgressManagerApp`クラスの`__init__`メソッド内で、以下の部分を変更します：

```python
# 6行のプログレス行を作成
self.progress_rows = []
for i in range(6):  # ←この数値を変更
    row = ProgressRow(main_frame, i + 1)
    self.progress_rows.append(row)
```

### デフォルト件数を変更する場合

`ProgressRow`クラスの`__init__`メソッド内で、以下の部分を変更します：

```python
self.max_entry.insert(0, "10")  # ←この数値を変更
self.max_value = 10  # ←この数値も変更
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

2.0.0
