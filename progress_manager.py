import tkinter as tk
from tkinter import ttk
import csv
import os


class ProgressRow:
    """各プログレス行を管理するクラス"""
    
    def __init__(self, parent, row_number):
        self.row_number = row_number
        self.current_value = 0
        self.max_value = 10
        
        # 行のフレーム
        self.frame = ttk.Frame(parent, padding="5")
        self.frame.grid(row=row_number, column=0, sticky=(tk.W, tk.E), pady=0)
        
        # 業務内容入力
        ttk.Label(self.frame, text="業務内容:", width=8).grid(row=0, column=0, padx=(5, 2))
        self.name_entry = ttk.Entry(self.frame, width=35, font=('Arial', 10))
        self.name_entry.insert(0, f"項目 {row_number}")
        self.name_entry.grid(row=0, column=1, padx=(2, 2))
        
        # 件数入力
        ttk.Label(self.frame, text="件数:", width=8).grid(row=0, column=2, padx=(2, 2))
        self.max_entry = ttk.Entry(self.frame, width=5)
        self.max_entry.insert(0, "10")
        self.max_entry.bind('<KeyRelease>', self.on_max_changed)
        self.max_entry.grid(row=0, column=3, padx=(2, 2))
        
        # 現在値表示
        ttk.Label(self.frame, text="現在値:", width=8).grid(row=0, column=4, padx=(2, 2))
        self.current_label = ttk.Label(self.frame, text="0", width=10, 
                                       style='Current.TLabel')
        self.current_label.grid(row=0, column=5, padx=(2, 2))
        
        # ＋ボタン
        self.plus_btn = ttk.Button(self.frame, text="＋", width=3, 
                                   command=self.increment)
        self.plus_btn.grid(row=0, column=6, padx=1)
        
        # －ボタン
        self.minus_btn = ttk.Button(self.frame, text="－", width=3, 
                                    command=self.decrement)
        self.minus_btn.grid(row=0, column=7, padx=1)
        
        # 完了ボタン
        self.complete_btn = ttk.Button(self.frame, text="完了", width=6, 
                                       command=self.complete)
        self.complete_btn.grid(row=0, column=8, padx=1)
        
        # リセットボタン
        self.reset_btn = ttk.Button(self.frame, text="リセット", width=8, 
                                    command=self.reset)
        self.reset_btn.grid(row=0, column=9, padx=(1, 5))
        
        # プログレスバー
        self.progress_frame = ttk.Frame(self.frame)
        self.progress_frame.grid(row=1, column=0, columnspan=10, 
                                sticky=(tk.W, tk.E), pady=5)
        
        # キャンバスでプログレスバーを描画
        self.canvas = tk.Canvas(self.progress_frame, height=20, bg='white', 
                               relief='sunken', bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # パーセント表示
        self.percent_label = ttk.Label(self.progress_frame, text="0.0%", 
                                      font=('Arial', 10, 'bold'))
        self.percent_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # コメント欄
        comment_label_frame = ttk.Frame(self.frame)
        comment_label_frame.grid(row=2, column=0, columnspan=10, 
                                sticky=(tk.W, tk.E), pady=(3, 5))
        
        ttk.Label(comment_label_frame, text="コメント:", width=8).grid(row=0, column=0, padx=5, sticky=tk.W)
        
        # コメント入力用のTextウィジェット
        comment_frame = ttk.Frame(comment_label_frame)
        comment_frame.grid(row=0, column=1, columnspan=8, sticky=(tk.W, tk.E), padx=5)
        comment_frame.columnconfigure(0, weight=1)
        
        self.comment_text = tk.Text(comment_frame, height=1, width=50, wrap=tk.WORD)
        self.comment_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # コメント変更時の自動保存
        self.comment_text.bind('<KeyRelease>', self.on_comment_changed)
        
        # フレームの列の重み設定
        self.frame.columnconfigure(1, weight=1)
        comment_label_frame.columnconfigure(1, weight=1)
        
        self.update_progress()
    
    def get_max_value(self):
        """マックス値を取得"""
        try:
            value = int(self.max_entry.get())
            return max(1, value)  # 最小値は1
        except ValueError:
            return 10
    
    def on_max_changed(self, event=None):
        """マックス値が変更されたときの処理"""
        self.max_value = self.get_max_value()
        self.update_progress()
    
    def increment(self):
        """現在値を1増加"""
        max_val = self.get_max_value()
        if self.current_value < max_val:
            self.current_value += 1
            self.update_progress()
            self.on_value_changed()
    
    def decrement(self):
        """現在値を1減少"""
        if self.current_value > 0:
            self.current_value -= 1
            self.update_progress()
            self.on_value_changed()
    
    def complete(self):
        """現在値を件数の最大値に設定（100%にする）"""
        max_val = self.get_max_value()
        self.current_value = max_val
        self.update_progress()
        self.on_value_changed()
    
    def reset(self):
        """業務内容、件数、現在値、コメントをリセット"""
        # 業務内容をデフォルト値にリセット
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, f"項目 {self.row_number}")
        
        # 件数を10にリセット
        self.max_entry.delete(0, tk.END)
        self.max_entry.insert(0, "10")
        self.max_value = 10
        
        # 現在値を0にリセット
        self.current_value = 0
        
        # コメントをクリア
        self.comment_text.delete("1.0", tk.END)
        
        self.update_progress()
        self.on_value_changed()
    
    def on_value_changed(self):
        """値が変更されたときの処理（親に通知）"""
        if hasattr(self, 'parent_app') and self.parent_app:
            self.parent_app.save_to_csv()
            self.parent_app.update_summary()
    
    def on_comment_changed(self, event=None):
        """コメントが変更されたときの処理"""
        if hasattr(self, 'parent_app') and self.parent_app:
            self.parent_app.save_to_csv()
            self.parent_app.update_summary()
    
    def get_data(self):
        """この行のデータを取得"""
        return {
            'row_number': self.row_number,
            'item_name': self.name_entry.get(),
            'max_value': self.get_max_value(),
            'current_value': self.current_value,
            'comment': self.comment_text.get("1.0", tk.END).strip()
        }
    
    def set_data(self, item_name, max_value, current_value, comment=""):
        """この行にデータを設定"""
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item_name)
        
        self.max_entry.delete(0, tk.END)
        self.max_entry.insert(0, str(max_value))
        
        self.current_value = current_value
        
        self.comment_text.delete("1.0", tk.END)
        self.comment_text.insert("1.0", comment)
        
        self.update_progress()
    
    def update_progress(self):
        """プログレスバーを更新"""
        max_val = self.get_max_value()
        self.current_label.config(text=str(self.current_value))
        
        # パーセンテージ計算
        if max_val > 0:
            percentage = (self.current_value / max_val) * 100
        else:
            percentage = 0
        
        self.percent_label.config(text=f"{percentage:.1f}%")
        
        # プログレスバーの描画
        self.draw_progress_bar(percentage)
    
    def draw_progress_bar(self, percentage):
        """プログレスバーをキャンバスに描画"""
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 初期化時のサイズが0の場合のデフォルト値
        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 30
        
        # バーの幅を計算
        bar_width = (canvas_width * percentage) / 100
        
        # 背景（グレー）
        self.canvas.create_rectangle(0, 0, canvas_width, canvas_height, 
                                     fill='#E0E0E0', outline='')
        
        # プログレスバーの色を達成度によって変更
        if percentage >= 100:
            bar_color = '#4CAF50'  # 緑（完了）
        elif percentage >= 75:
            bar_color = '#8BC34A'  # 黄緑
        elif percentage >= 50:
            bar_color = '#FFC107'  # 黄色
        elif percentage >= 25:
            bar_color = '#FF9800'  # オレンジ
        else:
            bar_color = '#2196F3'  # 青
        
        # プログレスバー描画
        if bar_width > 0:
            self.canvas.create_rectangle(0, 0, bar_width, canvas_height, 
                                        fill=bar_color, outline='')


class ProgressManagerApp:
    """プログレス管理アプリケーションのメインクラス"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("業務進捗管理")
        self.root.geometry("600x755")
        self.csv_filename = "progress_data.csv"
        
        # スタイル設定
        style = ttk.Style()
        style.configure('Current.TLabel', font=('Arial', 10, 'bold'), 
                       foreground='#2196F3')
        
        # メインフレーム
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル行フレーム
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # タイトル
        title_label = ttk.Label(title_frame, text="業務進捗管理", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 右上の小窓（コピペ用表示）
        summary_frame = ttk.LabelFrame(title_frame, text="入力済み項目", padding="3")
        summary_frame.grid(row=0, column=1, sticky=(tk.N, tk.E), padx=(20, 0))
        
        # コピペ可能なテキストフィールド（小さく）
        self.summary_text = tk.Text(summary_frame, width=25, height=4, 
                                   wrap=tk.WORD, font=('Arial', 8))
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # タイトル行の列の重み設定
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)
        
        # 6行のプログレス行を作成
        self.progress_rows = []
        for i in range(6):
            row = ProgressRow(main_frame, i + 1)
            row.parent_app = self  # 親アプリへの参照を設定
            self.progress_rows.append(row)
        
        # 全体リセットボタン
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=7, column=0, pady=(0, 10))
        
        reset_all_btn = ttk.Button(button_frame, text="全てリセット", 
                                   command=self.reset_all, 
                                   style='Accent.TButton')
        reset_all_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = ttk.Button(button_frame, text="終了", 
                             command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # グリッドの重み設定
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # ウィンドウリサイズ時にプログレスバーを再描画
        self.root.bind('<Configure>', self.on_resize)
        
        # ウィンドウ終了時の処理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # CSVファイルから前回のデータを読み込み
        self.load_from_csv()
        
        # サマリー表示を初期化
        self.update_summary()
    
    def reset_all(self):
        """全ての行をリセット"""
        for row in self.progress_rows:
            row.reset()
    
    def on_resize(self, event=None):
        """ウィンドウリサイズ時の処理"""
        # 少し遅延させて再描画
        self.root.after(50, self.redraw_all)
    
    def redraw_all(self):
        """全てのプログレスバーを再描画"""
        for row in self.progress_rows:
            row.update_progress()
    
    def save_to_csv(self):
        """現在の進捗状況をCSVファイルに保存"""
        try:
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['row_number', 'item_name', 'max_value', 'current_value', 'comment'])
                
                for row in self.progress_rows:
                    data = row.get_data()
                    writer.writerow([
                        data['row_number'],
                        data['item_name'],
                        data['max_value'],
                        data['current_value'],
                        data['comment']
                    ])
        except Exception as e:
            print(f"CSV保存エラー: {e}")
    
    def load_from_csv(self):
        """CSVファイルから進捗状況を読み込み"""
        if not os.path.exists(self.csv_filename):
            return
        
        try:
            with open(self.csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row_data in reader:
                    row_number = int(row_data['row_number'])
                    if 1 <= row_number <= len(self.progress_rows):
                        idx = row_number - 1
                        # コメント欄が存在しない古いCSVファイルに対応
                        comment = row_data.get('comment', '')
                        self.progress_rows[idx].set_data(
                            row_data['item_name'],
                            int(row_data['max_value']),
                            int(row_data['current_value']),
                            comment
                        )
            print(f"前回のデータを読み込みました: {self.csv_filename}")
        except Exception as e:
            print(f"CSV読み込みエラー: {e}")
    
    def update_summary(self):
        """入力済み項目のサマリーを更新"""
        lines = []
        for row in self.progress_rows:
            data = row.get_data()
            # 現在値が0より大きい、またはコメントがある行のみ表示
            if data['current_value'] > 0 or data['comment'].strip():
                item_name = data['item_name']
                count = data['current_value']
                comment = data['comment'].strip()
                if comment:
                    lines.append(f"{item_name}：{count}　{comment}")
                else:
                    lines.append(f"{item_name}：{count}")
        
        # テキストフィールドを更新
        self.summary_text.delete("1.0", tk.END)
        if lines:
            self.summary_text.insert("1.0", "\n".join(lines))
    
    def on_closing(self):
        """ウィンドウを閉じる際の処理"""
        self.save_to_csv()
        self.root.destroy()


def main():
    """メイン関数"""
    root = tk.Tk()
    app = ProgressManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

