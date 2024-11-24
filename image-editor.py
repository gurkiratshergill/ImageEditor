import tkinter as tk
from PIL import ImageTk, Image, ImageFilter, ImageOps
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Main Window
root = tk.Tk()
root.geometry("1200x800")
root.title("Image Editor")
frame = tk.Frame(root)
frame.pack(side="top", fill=tk.X)
rightFrame = tk.Frame(root)
rightFrame.pack(side="right", padx=10, pady=10, expand=True, fill=tk.BOTH)

pickedOption = tk.StringVar()
pickedOption.set('')
imagePath = ''
resize_Value_x = rightFrame.winfo_width()
resize_Value_y = rightFrame.winfo_height()
global edited_image, crop_rectangle, start_x, start_y, end_x, end_y, img_display, history
start_x = start_y = end_x = end_y = None
crop_rectangle = None
history = []  # History of image states

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def display_image_on_canvas(img):
    global img_display
    img_display = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=img_display)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

# Filters
def apply_sepia(img):
    return ImageOps.colorize(img.convert("L"), "#704214", "#C0A080")

def editImage():
    global imagePath, edited_image
    if imagePath:
        history.append(edited_image.copy())
        with Image.open(imagePath) as img:
            if pickedOption.get() == "Greyscale":
                edited_image = img.convert('L')
            elif pickedOption.get() == "Blur":
                edited_image = img.filter(ImageFilter.BLUR)
            elif pickedOption.get() == "Detail":
                edited_image = img.filter(ImageFilter.DETAIL)
            elif pickedOption.get() == "Sepia":
                edited_image = apply_sepia(img)
            elif pickedOption.get() == "Edge Enhance":
                edited_image = img.filter(ImageFilter.EDGE_ENHANCE)
            elif pickedOption.get() == "Emboss":
                edited_image = img.filter(ImageFilter.EMBOSS)

            max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
            edited_image_resized = resize_image(edited_image, max_width, max_height)
            display_image_on_canvas(edited_image_resized)

def saveImage():
    global edited_image
    if edited_image:
        edited_image.save("copy.jpg", "JPEG")

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename

# Resize based on given size
def resize_image(img, max_width, max_height):
    width_ratio = max_width / img.width
    height_ratio = max_height / img.height
    ratio = min(width_ratio, height_ratio)
    new_width = int(img.width * ratio)
    new_height = int(img.height * ratio)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Opening file from local storage
def open_img():
    global imagePath, edited_image, img_display, history
    x = openfn()
    imagePath = x
    img = Image.open(x)

    max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
    img_resized = resize_image(img, max_width, max_height)
    display_image_on_canvas(img_resized)

    # Save the original image for editing
    edited_image = Image.open(imagePath)
    history.clear()  # Clear history when a new image is opened
    history.append(edited_image.copy())  # Save the original image to history

# Crop functionality
def start_crop(event):
    global start_x, start_y, crop_rectangle
    start_x, start_y = event.x, event.y
    if crop_rectangle is not None:
        canvas.delete(crop_rectangle)

def draw_crop_rectangle(event):
    global end_x, end_y, crop_rectangle
    end_x, end_y = event.x, event.y
    if crop_rectangle is not None:
        canvas.delete(crop_rectangle)
    crop_rectangle = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='red')

def crop_image():
    global edited_image, start_x, start_y, end_x, end_y, history, crop_rectangle
    if edited_image and all([start_x, start_y, end_x, end_y]):
        history.append(edited_image.copy())

        image_width, image_height = edited_image.size
        canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
        scale = min(canvas_width / image_width, canvas_height / image_height)
        img_start_x, img_start_y = int(start_x / scale), int(start_y / scale)
        img_end_x, img_end_y = int(end_x / scale), int(end_y / scale)
        edited_image = edited_image.crop((img_start_x, img_start_y, img_end_x, img_end_y))

        start_x = start_y = end_x = end_y = None
        if crop_rectangle is not None:
            canvas.delete(crop_rectangle)
            crop_rectangle = None

        max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
        display_image_on_canvas(resize_image(edited_image, max_width, max_height))

# Undo the last crop operation
def undo_crop(event=None):
    global edited_image, history
    if len(history) > 1:
        history.pop()
        edited_image = history[-1]
        max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
        display_image_on_canvas(resize_image(edited_image, max_width, max_height))

# Rotate Image
def rotate_image():
    global edited_image, history
    if edited_image:
        history.append(edited_image.copy())
        edited_image = edited_image.rotate(-90, expand=True)
        max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
        display_image_on_canvas(resize_image(edited_image, max_width, max_height))

# Flip Image
def flip_image(direction):
    global edited_image, history
    if edited_image:
        history.append(edited_image.copy())
        if direction == "horizontal":
            edited_image = edited_image.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == "vertical":
            edited_image = edited_image.transpose(Image.FLIP_TOP_BOTTOM)
        max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
        display_image_on_canvas(resize_image(edited_image, max_width, max_height))

# Reset Image
def reset_image():
    global edited_image, history
    if history:
        edited_image = history[0]
        history.clear()
        history.append(edited_image.copy())
        max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
        display_image_on_canvas(resize_image(edited_image, max_width, max_height))

# Menu button for file opening
fileBttn = ttk.Menubutton(frame, text="File")
Menu1 = ttk.Menu(fileBttn, tearoff=0)
Menu1.add_command(label="Open file", command=open_img)
fileBttn["menu"] = Menu1
fileBttn.pack(padx=10, pady=10)

# Left side option bar for picking an option to edit image
leftFrame = tk.Frame(root)
leftFrame.pack(side="left", fill=tk.Y)
pickedOption = tk.StringVar()
RadioButton = ttk.Radiobutton(leftFrame, text="Greyscale", variable=pickedOption, value="Greyscale")
RadioButton2 = ttk.Radiobutton(leftFrame, text="Blur", variable=pickedOption, value="Blur")
RadioButton3 = ttk.Radiobutton(leftFrame, text="Detail", variable=pickedOption, value="Detail")
RadioButton4 = ttk.Radiobutton(leftFrame, text="Sepia", variable=pickedOption, value="Sepia")
RadioButton5 = ttk.Radiobutton(leftFrame, text="Edge Enhance", variable=pickedOption, value="Edge Enhance")
RadioButton6 = ttk.Radiobutton(leftFrame, text="Emboss", variable=pickedOption, value="Emboss")
RadioButton.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
RadioButton2.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
RadioButton3.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
RadioButton4.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
RadioButton5.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
RadioButton6.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

applyButton = ttk.Button(leftFrame, text="Apply", command=editImage)
applyButton.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

rotateButton = ttk.Button(leftFrame, text="Rotate", command=rotate_image)
rotateButton.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

flipHButton = ttk.Button(leftFrame, text="Flip Horizontal", command=lambda: flip_image("horizontal"))
flipHButton.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

flipVButton = ttk.Button(leftFrame, text="Flip Vertical", command=lambda: flip_image("vertical"))
flipVButton.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

resetButton = ttk.Button(leftFrame, text="Reset", command=reset_image)
resetButton.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

saveButton = ttk.Button(leftFrame, text="Save", command=saveImage)
saveButton.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

cropButton = ttk.Button(leftFrame, text="Crop", command=crop_image)
cropButton.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

# Main canvas for displaying the image
canvas = tk.Canvas(rightFrame)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", start_crop)
canvas.bind("<B1-Motion>", draw_crop_rectangle)
root.bind("<Control-z>", undo_crop)

root.mainloop()
