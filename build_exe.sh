#!/bin/bash

echo "========================================"
echo "プログレス管理アプリ EXE化スクリプト"
echo "========================================"
echo ""

# PyInstallerがインストールされているか確認
if ! python -m pip show pyinstaller > /dev/null 2>&1; then
    echo "PyInstallerがインストールされていません。"
    echo "インストール中..."
    python -m pip install pyinstaller
fi

echo ""
echo "EXEファイルを作成中..."
echo ""

# PyInstallerでEXE化
pyinstaller --onefile --windowed --name "プログレス管理アプリ" progress_manager.py

echo ""
echo "========================================"
echo "EXE化が完了しました！"
echo "実行ファイルは dist フォルダ内にあります。"
echo "========================================"

