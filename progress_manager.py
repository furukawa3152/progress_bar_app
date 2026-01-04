import tkinter as tk
from tkinter import ttk
import csv
import os


class ProgressRow:
    """各プログレス行を管理するクラス"""
    
    def __init__(self, parent, row_number):
        self.row_number = row_number
        self.current_value = 0
        self.max_value = 100
        
        # 行のフレーム
        self.frame = ttk.Frame(parent, padding="5")
        self.frame.grid(row=row_number, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 項目名入力
        ttk.Label(self.frame, text="項目名:", width=8).grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(self.frame, width=15)
        self.name_entry.insert(0, f"項目 {row_number}")
        self.name_entry.grid(row=0, column=1, padx=5)
        
        # マックス値入力
        ttk.Label(self.frame, text="最大値:", width=8).grid(row=0, column=2, padx=5)
        self.max_entry = ttk.Entry(self.frame, width=10)
        self.max_entry.insert(0, "100")
        self.max_entry.bind('<KeyRelease>', self.on_max_changed)
        self.max_entry.grid(row=0, column=3, padx=5)
        
        # 現在値表示
        ttk.Label(self.frame, text="現在値:", width=8).grid(row=0, column=4, padx=5)
        self.current_label = ttk.Label(self.frame, text="0", width=10, 
                                       style='Current.TLabel')
        self.current_label.grid(row=0, column=5, padx=5)
        
        # ＋ボタン
        self.plus_btn = ttk.Button(self.frame, text="＋", width=3, 
                                   command=self.increment)
        self.plus_btn.grid(row=0, column=6, padx=2)
        
        # －ボタン
        self.minus_btn = ttk.Button(self.frame, text="－", width=3, 
                                    command=self.decrement)
        self.minus_btn.grid(row=0, column=7, padx=2)
        
        # リセットボタン
        self.reset_btn = ttk.Button(self.frame, text="リセット", width=8, 
                                    command=self.reset)
        self.reset_btn.grid(row=0, column=8, padx=5)
        
        # プログレスバー
        self.progress_frame = ttk.Frame(self.frame)
        self.progress_frame.grid(row=1, column=0, columnspan=9, 
                                sticky=(tk.W, tk.E), pady=5)
        
        # キャンバスでプログレスバーを描画
        self.canvas = tk.Canvas(self.progress_frame, height=30, bg='white', 
                               relief='sunken', bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # パーセント表示
        self.percent_label = ttk.Label(self.progress_frame, text="0.0%", 
                                      font=('Arial', 10, 'bold'))
        self.percent_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.update_progress()
    
    def get_max_value(self):
        """マックス値を取得"""
        try:
            value = int(self.max_entry.get())
            return max(1, value)  # 最小値は1
        except ValueError:
            return 100
    
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
    
    def reset(self):
        """現在値をリセット"""
        self.current_value = 0
        self.update_progress()
        self.on_value_changed()
    
    def on_value_changed(self):
        """値が変更されたときの処理（親に通知）"""
        if hasattr(self, 'parent_app') and self.parent_app:
            self.parent_app.save_to_csv()
    
    def get_data(self):
        """この行のデータを取得"""
        return {
            'row_number': self.row_number,
            'item_name': self.name_entry.get(),
            'max_value': self.get_max_value(),
            'current_value': self.current_value
        }
    
    def set_data(self, item_name, max_value, current_value):
        """この行にデータを設定"""
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item_name)
        
        self.max_entry.delete(0, tk.END)
        self.max_entry.insert(0, str(max_value))
        
        self.current_value = current_value
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
        self.root.title("プログレス管理")
        self.root.geometry("600x600")
        self.csv_filename = "progress_data.csv"
        
        # スタイル設定
        style = ttk.Style()
        style.configure('Current.TLabel', font=('Arial', 10, 'bold'), 
                       foreground='#2196F3')
        
        # メインフレーム
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(main_frame, text="プログレス管理", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # 5行のプログレス行を作成
        self.progress_rows = []
        for i in range(5):
            row = ProgressRow(main_frame, i + 1)
            row.parent_app = self  # 親アプリへの参照を設定
            self.progress_rows.append(row)
        
        # 全体リセットボタン
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=7, column=0, pady=10)
        
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
                writer.writerow(['row_number', 'item_name', 'max_value', 'current_value'])
                
                for row in self.progress_rows:
                    data = row.get_data()
                    writer.writerow([
                        data['row_number'],
                        data['item_name'],
                        data['max_value'],
                        data['current_value']
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
                        self.progress_rows[idx].set_data(
                            row_data['item_name'],
                            int(row_data['max_value']),
                            int(row_data['current_value'])
                        )
            print(f"前回のデータを読み込みました: {self.csv_filename}")
        except Exception as e:
            print(f"CSV読み込みエラー: {e}")
    
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

