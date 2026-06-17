import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import os
import threading
import time
import math

# ─── Theme ────────────────────────────────────────────────────────────────────
THEME = {
    "bg":          "#0F0F14",
    "surface":     "#1A1A24",
    "border":      "#2A2A3A",
    "accent":      "#7C6AFF",
    "accent2":     "#FF6AB0",
    "text":        "#E8E6FF",
    "subtext":     "#7A78A0",
    "btn_bg":      "#1E1E2E",
    "btn_hover":   "#2E2E4A",
    "btn_active":  "#7C6AFF",
}

TRANSITION_DURATION = 0.5   # seconds
SLIDE_INTERVAL      = 5     # seconds
IMAGE_SIZE          = (1280, 780)


class PhotoSlideshow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Photo Slideshow")
        self.configure(bg=THEME["bg"])
        self.resizable(True, True)

        # ── State ──
        self.images          = []      # PIL Images
        self.photo_refs      = []      # ImageTk refs (prevent GC)
        self.current_index   = 0
        self.is_playing      = False
        self.is_fullscreen   = False
        self.after_id        = None
        self.transitioning   = False
        self.image_paths     = []

        # Displayed image size (updated on resize)
        self.disp_w, self.disp_h = IMAGE_SIZE

        self._build_ui()
        self.bind("<Configure>", self._on_resize)
        self.bind("<Escape>",    lambda e: self.exit_fullscreen())
        self.bind("<Left>",      lambda e: self.prev_image())
        self.bind("<Right>",     lambda e: self.next_image())
        self.bind("<space>",     lambda e: self.toggle_play())
        self.bind("<f>",         lambda e: self.toggle_fullscreen())

        self._show_empty_state()

    # ─────────────────────────────────────────────────────── UI BUILD ─────────

    def _build_ui(self):
        # ── Top bar ──
        self.top_bar = tk.Frame(self, bg=THEME["surface"], height=52)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        tk.Label(
            self.top_bar, text="✦ SLIDESHOW",
            bg=THEME["surface"], fg=THEME["accent"],
            font=("Helvetica", 13, "bold"), padx=20
        ).pack(side="left", pady=12)

        self.folder_btn = self._make_top_btn(
            self.top_bar, "📁  Open Folder", self.open_folder, side="left"
        )
        self.fs_btn = self._make_top_btn(
            self.top_bar, "⛶  Fullscreen", self.toggle_fullscreen, side="right"
        )

        self.img_counter = tk.Label(
            self.top_bar, text="",
            bg=THEME["surface"], fg=THEME["subtext"],
            font=("Helvetica", 11), padx=16
        )
        self.img_counter.pack(side="right", pady=12)

        # ── Canvas ──
        self.canvas = tk.Canvas(
            self, bg=THEME["bg"],
            highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0)

        # ── Bottom control bar ──
        self.ctrl_bar = tk.Frame(self, bg=THEME["surface"], height=72)
        self.ctrl_bar.pack(fill="x", side="bottom")
        self.ctrl_bar.pack_propagate(False)

        # Progress track
        self.progress_frame = tk.Frame(self, bg=THEME["border"], height=2)
        self.progress_frame.pack(fill="x", side="bottom")

        self.progress_bar = tk.Frame(self.progress_frame, bg=THEME["accent"], height=2)
        self.progress_bar.place(x=0, y=0, width=0, relheight=1)

        # Controls
        center = tk.Frame(self.ctrl_bar, bg=THEME["surface"])
        center.pack(expand=True)

        self.prev_btn  = self._make_ctrl_btn(center, "⏮", self.prev_image)
        self.play_btn  = self._make_ctrl_btn(center, "▶", self.toggle_play, big=True)
        self.next_btn  = self._make_ctrl_btn(center, "⏭", self.next_image)

        # Interval selector (right side)
        right = tk.Frame(self.ctrl_bar, bg=THEME["surface"])
        right.place(relx=1.0, rely=0.5, anchor="e", x=-20)

        tk.Label(
            right, text="INTERVAL",
            bg=THEME["surface"], fg=THEME["subtext"],
            font=("Helvetica", 8)
        ).pack()

        self.interval_var = tk.IntVar(value=SLIDE_INTERVAL)
        interval_spin = tk.Spinbox(
            right, from_=1, to=30, textvariable=self.interval_var,
            width=4, justify="center",
            bg=THEME["btn_bg"], fg=THEME["text"],
            buttonbackground=THEME["btn_bg"],
            relief="flat", font=("Helvetica", 13),
            highlightthickness=1, highlightcolor=THEME["accent"],
            highlightbackground=THEME["border"]
        )
        interval_spin.pack()

        tk.Label(
            right, text="seconds",
            bg=THEME["surface"], fg=THEME["subtext"],
            font=("Helvetica", 8)
        ).pack()

        # Transition picker (left side)
        left = tk.Frame(self.ctrl_bar, bg=THEME["surface"])
        left.place(relx=0.0, rely=0.5, anchor="w", x=20)

        tk.Label(
            left, text="TRANSITION",
            bg=THEME["surface"], fg=THEME["subtext"],
            font=("Helvetica", 8)
        ).pack()

        self.transition_var = tk.StringVar(value="Fade")
        for t in ("Fade", "Slide", "Zoom"):
            rb = tk.Radiobutton(
                left, text=t, variable=self.transition_var, value=t,
                bg=THEME["surface"], fg=THEME["subtext"],
                selectcolor=THEME["btn_bg"],
                activebackground=THEME["surface"],
                activeforeground=THEME["accent"],
                font=("Helvetica", 9),
                indicatoron=True,
                relief="flat"
            )
            rb.pack(anchor="w")

    def _make_top_btn(self, parent, text, cmd, side="left"):
        btn = tk.Label(
            parent, text=text,
            bg=THEME["surface"], fg=THEME["text"],
            font=("Helvetica", 11), padx=14, pady=14,
            cursor="hand2"
        )
        btn.pack(side=side)
        btn.bind("<Enter>",   lambda e: btn.config(fg=THEME["accent"]))
        btn.bind("<Leave>",   lambda e: btn.config(fg=THEME["text"]))
        btn.bind("<Button-1>", lambda e: cmd())
        return btn

    def _make_ctrl_btn(self, parent, text, cmd, big=False):
        size   = 52 if big else 42
        radius = 26 if big else 21
        font   = ("Helvetica", 20 if big else 15)
        bg     = THEME["accent"] if big else THEME["btn_bg"]
        fg     = "#FFFFFF"

        btn = tk.Label(
            parent, text=text,
            bg=bg, fg=fg,
            font=font,
            width=2, padx=10 if big else 8, pady=6,
            cursor="hand2", relief="flat"
        )
        btn.pack(side="left", padx=6, pady=12)

        def on_enter(e):
            btn.config(bg=THEME["accent2"] if big else THEME["btn_hover"])
        def on_leave(e):
            btn.config(bg=THEME["accent"] if big else THEME["btn_bg"])

        btn.bind("<Enter>",    on_enter)
        btn.bind("<Leave>",    on_leave)
        btn.bind("<Button-1>", lambda e: cmd())
        return btn

    # ─────────────────────────────────────────────────── EMPTY STATE ──────────

    def _show_empty_state(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()  or IMAGE_SIZE[0]
        h = self.canvas.winfo_height() or IMAGE_SIZE[1]
        cx, cy = w // 2, h // 2

        self.canvas.create_text(
            cx, cy - 30,
            text="📁",
            font=("Helvetica", 48),
            fill=THEME["border"], anchor="center"
        )
        self.canvas.create_text(
            cx, cy + 40,
            text="Open a folder to start your slideshow",
            font=("Helvetica", 16),
            fill=THEME["subtext"], anchor="center"
        )
        self.canvas.create_text(
            cx, cy + 70,
            text="← → to navigate  ·  Space to play/pause  ·  F for fullscreen",
            font=("Helvetica", 11),
            fill=THEME["border"], anchor="center"
        )

    # ─────────────────────────────────────────────────── FOLDER OPEN ──────────

    def open_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if not folder:
            return

        exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}
        paths = sorted([
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in exts
        ])

        if not paths:
            messagebox.showinfo("No Images", "No supported images found in that folder.")
            return

        self.is_playing = False
        self.play_btn.config(text="▶")
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.image_paths = paths
        self.images      = []
        self.photo_refs  = []
        self.current_index = 0

        # Load in background thread
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or IMAGE_SIZE[0]
        h = self.canvas.winfo_height() or IMAGE_SIZE[1]
        self.canvas.create_text(
            w // 2, h // 2,
            text=f"Loading {len(paths)} images…",
            font=("Helvetica", 16),
            fill=THEME["subtext"], anchor="center"
        )

        threading.Thread(target=self._load_images, args=(paths,), daemon=True).start()

    def _load_images(self, paths):
        imgs = []
        for p in paths:
            try:
                img = Image.open(p).convert("RGBA")
                imgs.append(img)
            except Exception:
                pass
        self.images = imgs
        self.after(0, self._on_images_loaded)

    def _on_images_loaded(self):
        if not self.images:
            messagebox.showerror("Error", "Could not load any images.")
            return
        self.current_index = 0
        self._update_counter()
        self._render_image(self.current_index)

    # ─────────────────────────────────────────────────── NAVIGATION ───────────

    def next_image(self):
        if not self.images or self.transitioning:
            return
        next_idx = (self.current_index + 1) % len(self.images)
        self._transition_to(next_idx)

    def prev_image(self):
        if not self.images or self.transitioning:
            return
        prev_idx = (self.current_index - 1) % len(self.images)
        self._transition_to(prev_idx)

    def toggle_play(self):
        if not self.images:
            return
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.config(text="⏸")
            self._schedule_next()
        else:
            self.play_btn.config(text="▶")
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None

    def _schedule_next(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        interval_ms = self.interval_var.get() * 1000
        self.after_id = self.after(interval_ms, self._auto_advance)
        self._animate_progress(interval_ms)

    def _auto_advance(self):
        if self.is_playing and self.images:
            next_idx = (self.current_index + 1) % len(self.images)
            self._transition_to(next_idx, auto=True)

    def _animate_progress(self, total_ms, elapsed=0):
        if not self.is_playing:
            self.progress_bar.place_configure(width=0)
            return
        frac     = min(elapsed / total_ms, 1.0)
        bar_w    = int(self.winfo_width() * frac)
        self.progress_bar.place_configure(width=bar_w)
        if elapsed < total_ms:
            self.after(50, self._animate_progress, total_ms, elapsed + 50)

    # ─────────────────────────────────────────────────── TRANSITIONS ──────────

    def _transition_to(self, new_index, auto=False):
        if self.transitioning:
            return
        self.transitioning  = True
        self.current_index  = new_index
        self._update_counter()

        mode = self.transition_var.get()
        if mode == "Fade":
            self._transition_fade(new_index, auto)
        elif mode == "Slide":
            self._transition_slide(new_index, auto)
        elif mode == "Zoom":
            self._transition_zoom(new_index, auto)

    def _get_canvas_dims(self):
        w = self.canvas.winfo_width()  or IMAGE_SIZE[0]
        h = self.canvas.winfo_height() or IMAGE_SIZE[1]
        return w, h

    def _fit_image(self, pil_img, w, h):
        """Return an RGBA PIL image fitted (letterboxed) to w×h."""
        img = pil_img.copy()
        img.thumbnail((w, h), Image.LANCZOS)
        result = Image.new("RGBA", (w, h), (15, 15, 20, 255))
        ox = (w - img.width)  // 2
        oy = (h - img.height) // 2
        result.paste(img, (ox, oy))
        return result

    # ── Fade ──
    def _transition_fade(self, idx, auto, step=0, steps=20):
        w, h    = self._get_canvas_dims()
        new_pil = self._fit_image(self.images[idx], w, h)

        if step == 0:
            # snapshot current canvas content as image
            try:
                self._fade_old = self._current_pil.copy()
            except AttributeError:
                self._fade_old = Image.new("RGBA", (w, h), (15, 15, 20, 255))

        alpha = int(255 * step / steps)
        blended = Image.blend(self._fade_old, new_pil, step / steps)
        tk_img = ImageTk.PhotoImage(blended)
        self.photo_refs = [tk_img]
        self.canvas.delete("all")
        self.canvas.create_image(w // 2, h // 2, image=tk_img, anchor="center")

        if step < steps:
            self.after(int(TRANSITION_DURATION * 1000 / steps),
                       self._transition_fade, idx, auto, step + 1, steps)
        else:
            self._current_pil = new_pil
            self.transitioning = False
            if auto and self.is_playing:
                self._schedule_next()

    # ── Slide ──
    def _transition_slide(self, idx, auto, step=0, steps=20):
        w, h    = self._get_canvas_dims()
        new_pil = self._fit_image(self.images[idx], w, h)

        if step == 0:
            try:
                self._slide_old = self._current_pil.copy()
            except AttributeError:
                self._slide_old = Image.new("RGBA", (w, h), (15, 15, 20, 255))

        # Ease in-out cubic
        t    = step / steps
        ease = t * t * (3 - 2 * t)
        offset = int(w * ease)

        combined = Image.new("RGBA", (w, h), (15, 15, 20, 255))
        combined.paste(self._slide_old, (-offset, 0))
        combined.paste(new_pil, (w - offset, 0))

        tk_img = ImageTk.PhotoImage(combined)
        self.photo_refs = [tk_img]
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=tk_img, anchor="nw")

        if step < steps:
            self.after(int(TRANSITION_DURATION * 1000 / steps),
                       self._transition_slide, idx, auto, step + 1, steps)
        else:
            self._current_pil = new_pil
            self.transitioning = False
            if auto and self.is_playing:
                self._schedule_next()

    # ── Zoom ──
    def _transition_zoom(self, idx, auto, step=0, steps=20):
        w, h    = self._get_canvas_dims()
        new_pil = self._fit_image(self.images[idx], w, h)

        t    = step / steps
        ease = t * t * (3 - 2 * t)
        scale = 1.0 + 0.08 * (1 - ease)

        zoomed_w = int(w * scale)
        zoomed_h = int(h * scale)
        new_scaled = new_pil.resize((zoomed_w, zoomed_h), Image.LANCZOS)
        ox = (zoomed_w - w) // 2
        oy = (zoomed_h - h) // 2
        cropped = new_scaled.crop((ox, oy, ox + w, oy + h))

        alpha_img = cropped.copy()
        alpha_val = int(255 * ease)
        r, g, b, a = alpha_img.split()
        a = a.point(lambda p: min(p, alpha_val))
        alpha_img = Image.merge("RGBA", (r, g, b, a))

        try:
            base = self._current_pil.copy()
        except AttributeError:
            base = Image.new("RGBA", (w, h), (15, 15, 20, 255))

        combined = Image.alpha_composite(base, alpha_img)

        tk_img = ImageTk.PhotoImage(combined)
        self.photo_refs = [tk_img]
        self.canvas.delete("all")
        self.canvas.create_image(w // 2, h // 2, image=tk_img, anchor="center")

        if step < steps:
            self.after(int(TRANSITION_DURATION * 1000 / steps),
                       self._transition_zoom, idx, auto, step + 1, steps)
        else:
            self._current_pil = new_pil
            self.transitioning = False
            if auto and self.is_playing:
                self._schedule_next()

    # ─────────────────────────────────────────────────── RENDER / RESIZE ──────

    def _render_image(self, idx):
        if not self.images:
            return
        w, h    = self._get_canvas_dims()
        pil_img = self._fit_image(self.images[idx], w, h)
        tk_img  = ImageTk.PhotoImage(pil_img)
        self.photo_refs = [tk_img]
        self._current_pil = pil_img
        self.canvas.delete("all")
        self.canvas.create_image(w // 2, h // 2, image=tk_img, anchor="center")

    def _on_resize(self, event):
        if event.widget is self and self.images:
            self._render_image(self.current_index)

    # ─────────────────────────────────────────────────── FULLSCREEN ───────────

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.fs_btn.config(text="✕  Exit" if self.is_fullscreen else "⛶  Fullscreen")
        if self.images:
            self.after(50, lambda: self._render_image(self.current_index))

    def exit_fullscreen(self):
        if self.is_fullscreen:
            self.toggle_fullscreen()

    # ─────────────────────────────────────────────────── COUNTER ─────────────

    def _update_counter(self):
        if self.images:
            self.img_counter.config(
                text=f"{self.current_index + 1} / {len(self.images)}"
            )
        else:
            self.img_counter.config(text="")

    # ─────────────────────────────────────────────────── EXTRA: MOUSE HINTS ───

    def _bind_canvas_hints(self):
        self.canvas.bind("<Button-1>", lambda e: self.next_image())


if __name__ == "__main__":
    app = PhotoSlideshow()
    app.geometry("1280x860")
    app.mainloop()