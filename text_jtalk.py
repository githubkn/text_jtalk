# Open JTalkテキスト読み上げツール for Windows
# 起動方法：
# >python text_jtalk.py

# 2020/3/31 ver 1.0 1stリリース

import tkinter as tk
from tkinter import ttk
import subprocess
import winsound
import glob

tool_base = r'C:\open_jtalk' + '\\'         # open_jtalk.exeが存在するフォルダ
voice_base = tool_base + 'voice' + '\\'     # *.htsvoiceファイルが存在フォルダ

def get_cmd_strs(voice, out_file):
    """
        コマンド文字列の生成
        @param voice    .htsvoiceファイル
        @param out_file 出力ファイル
    """
    global tool_base
    open_jtalk = [tool_base + r'bin\open_jtalk']
    dic = ['-x', tool_base + 'dic']
    htsvoice = ['-m', voice]
    speed = ['-r', '1.0']
    outwav = ['-ow', out_file]
    return(open_jtalk+dic+htsvoice+speed+outwav)

def play_wav(wav_file):
    """
        音声を鳴らす
        @param wav_file 音声ファイルのパス
    """
    winsound.PlaySound(wav_file, winsound.SND_FILENAME | winsound.SND_ASYNC )

def stop_wav():
    """
        音声を止める
    """
    winsound.PlaySound( None, winsound.SND_PURGE )

def output_talk_wav(cmd, txt):
    """
        コマンド文字列の生成
        @param cmd open_jtalkコマンドライン文字列
        @param t   話す内容
    """
    res = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    res.stdin.write(txt.encode('Shift_JIS'))
    res.stdin.close()
    res.wait()

def b1_clicked():
    """
        再生ボタン押下イベント
    """
    cmd = get_cmd_strs(cb_str.get(), 'out.wav')
    global txt_str
    txt_str = txt.get('1.0', tk.END)      # テキストボックス内容取得
    txt_str = txt_str.replace("\n", " ")   # 改行をスペースに
    output_talk_wav(cmd, txt_str)
    play_wav('out.wav')

def b2_clicked():
    """
        停止ボタン押下イベント
    """
    stop_wav()

top = tk.Tk()
top.title('Open JTalkテキスト読み上げツール')
top.minsize(100, 100)
top.geometry('400x200')

# Frame
f = ttk.Frame(top, padding=5)
f.pack(expand=True, fill='both')

# Text
#txt = tk.Text(f, width=80, height=10)
txt = tk.Text(f, width=0, height=0)
txt.pack(expand=True, fill='both', side='left')

# Scrollbar
sc = ttk.Scrollbar(
        f,
        orient=tk.VERTICAL,
        command=txt.yview)
txt['yscrollcommand'] = sc.set
sc.pack(side='left', fill='y')

# Combobox
f2 = ttk.Frame(top, padding=5)
f2.pack(fill='x')

cb_str = tk.StringVar()
cb = ttk.Combobox(f2, textvariable=cb_str)
cb.pack(fill='x')

cb['values'] = glob.glob(voice_base + "*.htsvoice")

cb.current(0)

# Button
f3 = ttk.Frame(top, padding=0)
f3.pack()

b1 = ttk.Button(f3, text='再生', command=b1_clicked)
b2 = ttk.Button(f3, text='停止', command=b2_clicked)
b1.pack(side='left')
b2.pack(side='left')

top.mainloop()
