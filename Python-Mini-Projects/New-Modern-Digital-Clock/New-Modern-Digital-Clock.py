import tkinter as tk
from time import strftime
from datetime import datetime

root = tk.Tk()
root.title("Digital Clock")
root.configure(bg='#0a0a0a')

ON  = '#e070ff'
DIM = '#1e061e'
W, H = 130, 220
PAD, THICK, GAP = 14, 18, 5

SEGS = {
    0:[1,1,1,0,1,1,1], 1:[0,0,1,0,0,1,0], 2:[1,0,1,1,1,0,1],
    3:[1,0,1,1,0,1,1], 4:[0,1,1,1,0,1,0], 5:[1,1,0,1,0,1,1],
    6:[1,1,0,1,1,1,1], 7:[1,0,1,0,0,1,0], 8:[1,1,1,1,1,1,1],
    9:[1,1,1,1,0,1,1],
}

def draw_digit(canvas, num):
    canvas.delete('all')
    s = SEGS.get(num, [0]*7)
    mid = H // 2

    def h_seg(y, on):
        canvas.create_line(PAD+GAP, y, W-PAD-GAP, y,
                           fill=ON if on else DIM, width=THICK, capstyle='round')

    def v_seg(x, y, on):
        canvas.create_line(x, y+GAP, x, y+(mid-PAD)-GAP,
                           fill=ON if on else DIM, width=THICK, capstyle='round')

    h_seg(PAD,        s[0])
    v_seg(PAD,  PAD,  s[1])
    v_seg(W-PAD,PAD,  s[2])
    h_seg(mid,        s[3])
    v_seg(PAD,  mid,  s[4])
    v_seg(W-PAD,mid,  s[5])
    h_seg(H-PAD,      s[6])

digits = []
colons = []

frame = tk.Frame(root, bg='#0a0a0a')
frame.pack(expand=True)

def make_digit():
    c = tk.Canvas(frame, width=W, height=H, bg='#0a0a0a', highlightthickness=0)
    return c

def make_colon():
    f = tk.Frame(frame, bg='#0a0a0a', width=30, height=H)
    f.pack_propagate(False)
    top = tk.Canvas(f, width=16, height=16, bg='#0a0a0a', highlightthickness=0)
    bot = tk.Canvas(f, width=16, height=16, bg='#0a0a0a', highlightthickness=0)
    top.place(x=7, y=62)
    bot.place(x=7, y=128)
    top.create_oval(1,1,15,15, fill=ON, outline='')
    bot.create_oval(1,1,15,15, fill=ON, outline='')
    return f, top, bot

for i in range(6):
    d = make_digit()
    d.grid(row=0, column=i*2, padx=4)
    digits.append(d)
    if i in (1, 3):
        col_frame, t, b = make_colon()
        col_frame.grid(row=0, column=i*2+1, padx=0)
        colons.append((t, b))

ampm_frame = tk.Frame(frame, bg='#0a0a0a')
ampm_frame.grid(row=0, column=13, padx=(10,0))
am_lbl = tk.Label(ampm_frame, text='AM', font=('Courier', 16, 'bold'),
                  bg='#1a0a1a', fg='#2a0a2a', padx=8, pady=4)
am_lbl.pack(pady=(60,6))
pm_lbl = tk.Label(ampm_frame, text='PM', font=('Courier', 16, 'bold'),
                  bg='#1a0a1a', fg='#2a0a2a', padx=8, pady=4)
pm_lbl.pack()

date_lbl = tk.Label(root, font=('Courier', 18), bg='#0a0a0a', fg='#9940bb')
date_lbl.pack(pady=(0, 10))

snooze_btn = tk.Label(root, text='SNOOZE', font=('Courier', 11, 'bold'),
                      bg='#1a1a1a', fg='#555555', padx=24, pady=7)
snooze_btn.pack(pady=(0, 20))

def tick():
    now_h = int(strftime('%I'))
    now_m = int(strftime('%M'))
    now_s = int(strftime('%S'))
    is_pm = strftime('%p') == 'PM'
    blink = now_s % 2 == 0

    time_digits = [
        now_h // 10, now_h % 10,
        now_m // 10, now_m % 10,
        now_s // 10, now_s % 10,
    ]
    for i, d in enumerate(time_digits):
        draw_digit(digits[i], d)

    dot_color = ON if blink else DIM
    for top, bot in colons:
        top.create_oval(1,1,15,15, fill=dot_color, outline='')
        bot.create_oval(1,1,15,15, fill=dot_color, outline='')

    am_lbl.config(fg=ON if not is_pm else '#2a0a2a',
                  bg='#1f0a2a' if not is_pm else '#1a0a1a')
    pm_lbl.config(fg=ON if is_pm else '#2a0a2a',
                  bg='#1f0a2a' if is_pm else '#1a0a1a')

    days   = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    now = datetime.now()
    date_str = f"{days[now.weekday()]}    {months[now.month-1]} {now.day:02d}    {now.year}"
    date_lbl.config(text=date_str)

    root.after(1000, tick)

tick()

root.update_idletasks()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
w, h = 1440, 500
root.geometry(f'{w}x{h}+{(sw-w)//2}+{(sh-h)//2}')

root.mainloop()