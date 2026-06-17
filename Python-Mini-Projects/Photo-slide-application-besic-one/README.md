# 📸 Photo Slideshow Application

A simple and interactive **Photo Slideshow Application** built with **Python, Tkinter, and Pillow**. This desktop application displays a collection of images in an automated slideshow with a clean graphical interface.

---

## ✨ Features

- 🖼️ Display multiple images in a desktop GUI.
- 🔄 Automatic image transition using a slideshow mechanism.
- ⏳ Changes images automatically at a fixed time interval.
- ▶️ Start slideshow with a single button click.
- 🔁 Continuously loops through all images.
- 📏 Resizes images while maintaining their original aspect ratio.
- 🖥️ Simple and user-friendly interface.

---

## 🛠️ Technologies Used

- **Python**
- **Tkinter** – GUI development
- **Pillow (PIL)** – Image processing and image display
- **itertools.cycle** – Infinite looping through images

---

## 📂 Project Structure

```
Photo-Slideshow/
│
├── Photo-Slideshow.py
├── images/
│   ├── 1.jpeg
│   ├── 2.jpeg
│   ├── 3.jpeg
│   └── 4.jpeg
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-link>
```

### 2. Navigate to the Project Directory

```bash
cd Photo-Slideshow
```

### 3. Install Required Dependency

```bash
pip install pillow
```

### 4. Run the Application

```bash
python Photo-Slideshow.py
```

---

## ⚙️ How It Works

1. Images are loaded using the Pillow library.
2. Images are resized to fit the application window.
3. `ImageTk.PhotoImage` converts images into a Tkinter-compatible format.
4. Clicking the **Play Slideshow** button starts the slideshow.
5. Tkinter's `after()` method updates the image every 5 seconds.
6. `itertools.cycle` ensures the slideshow repeats continuously.

---

## 🧠 Concepts Covered

- GUI Development with Tkinter
- Event-Driven Programming
- Working with Buttons and Labels
- Image Handling with Pillow
- Using Iterators in Python
- Creating Timed Events using `after()`

---

## 📸 Preview

Add your application screenshot or GIF here.

```
![Photo Slideshow Preview](screenshot.png)
```

---

## 👩‍💻 Author

**Tanisha Islam**

Python Developer | UI/UX Designer | Data Science Student

---

⭐ If you found this project interesting, consider giving it a star on GitHub.