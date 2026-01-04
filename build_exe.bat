@echo off
echo ========================================
echo プログレス管理アプリ EXE化スクリプト
echo ========================================
echo.

REM PyInstallerがインストールされているか確認
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstallerがインストールされていません。
    echo インストール中...
    python -m pip install pyinstaller
)

echo.
echo EXEファイルを作成中...
echo.

REM PyInstallerでEXE化
pyinstaller --onefile --windowed --name "プログレス管理アプリ" --icon=NONE progress_manager.py

echo.
echo ========================================
echo EXE化が完了しました！
echo 実行ファイルは dist フォルダ内にあります。
echo ========================================
pause

