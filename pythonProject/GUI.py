import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import stacking
import analyze
import promptlib
import os


class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.image = None
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.crop_button = tk.Button(root, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()

        self.rect = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        root.mainloop()

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tif")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image, master = self.root)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y

    def crop_image(self):
        if self.image and self.rect:
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            print(x1, y1, x2, y2)
            # cropped_image = self.image.crop((x1, y1, x2, y2))
            # cropped_image.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.mainloop()

