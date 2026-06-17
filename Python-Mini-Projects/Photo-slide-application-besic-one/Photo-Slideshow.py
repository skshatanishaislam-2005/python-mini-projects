from itertools import cycle
from PIL import Image,ImageTk
import time
import tkinter as tk

root = tk.Tk()
root.title("Photo Sliding")
root.geometry("1380x1380")

image_paths = [
    r"/Users/apple/Downloads/Picture/2.jpeg",
    r"/Users/apple/Downloads/Picture/3.jpeg",
    r"/Users/apple/Downloads/Picture/4.jpeg",
    r"/Users/apple/Downloads/Picture/1.jpeg"
]

image_size = (1380,1380)
images = []

for path in image_paths:
    img = Image.open(path)
    img.thumbnail(image_size, Image.LANCZOS)
    images.append(img)

photo_images = [ImageTk.PhotoImage(img) for img in images]

label = tk.Label(root)
label.pack()

def update_image():
    photo_image = next(slideshow)
    label.config(image=photo_image)
    root.after(5000, update_image)



slideshow = cycle(photo_images)

def start_slideshow():
    update_image()

def start_slideshow():
    play_button.config(state=tk.DISABLED)
    update_image()

play_button = tk.Button(root, text = 'play slideshow', command= start_slideshow)
play_button.pack()

root.mainloop()


