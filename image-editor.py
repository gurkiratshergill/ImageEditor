import tkinter as tk
from PIL import ImageTk, Image
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
global edited_image

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def openFile():
    pass

def editImage():
    global imagePath
    global edited_image
    if imagePath:
        if pickedOption.get() == "Greyscale":
            with Image.open(imagePath) as img:
                blackAndWhite = img.convert('L')
                max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
                blackAndWhite = resize_image(blackAndWhite, max_width, max_height)
                edited_image = blackAndWhite
                blackAndWhite = ImageTk.PhotoImage(blackAndWhite)

            clear_frame(rightFrame)
            panel = tk.Label(rightFrame, image=blackAndWhite)
            panel.image = blackAndWhite
            panel.pack()

def resize_Image():
    pass

def saveImage():
    global imagePath
    global edited_image
    edited_image.save("copy.jpg", "JPEG")

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename

def resize_image(img, max_width, max_height):
    width_ratio = max_width / img.width
    height_ratio = max_height / img.height
    ratio = min(width_ratio, height_ratio)
    new_width = int(img.width * ratio)
    new_height = int(img.height * ratio)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def open_img():
    global imagePath
    x = openfn()
    imagePath = x
    img = Image.open(x)

    max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()

    img = resize_image(img, max_width, max_height)
    img = ImageTk.PhotoImage(img)
    clear_frame(rightFrame)
    panel = tk.Label(rightFrame, image=img)
    panel.image = img
    panel.pack()

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
RadioButton.grid(row=0, column=0,columnspan=2,padx=5,pady=5)
applyButton = ttk.Button(leftFrame, text="Apply", command=editImage)
applyButton.grid(row=1, column=0,columnspan=2,padx=5,pady=5)
resize_Label = ttk.Label(leftFrame, text="Resize")
resize_Label.grid(row=2, column=0,columnspan=2,padx=5,pady=5)
resize_x_value = ttk.Label(leftFrame, text="X=")
resize_Entry_x = ttk.Entry(leftFrame, textvariable=tk.StringVar(value=resize_Value_x))

resize_y_value = ttk.Label(leftFrame, text="Y=")
resize_Entry_y = ttk.Entry(leftFrame, textvariable=tk.StringVar(value=resize_Value_y))

resize_x_value.grid(row=3, column=0,padx=5,pady=5)
resize_Entry_x.grid(row=3, column=1,padx=5,pady=5)
resize_y_value.grid(row=4, column=0,padx=5,pady=5)
resize_Entry_y.grid(row=4, column=1,padx=5,pady=5)
resizeButton = ttk.Button(leftFrame, text="Resize", command=resize_Image)
resizeButton.grid(row=5,column=0,columnspan=2,padx=5,pady=5)

saveButton = ttk.Button(leftFrame, text="Save Copy", command=saveImage)
saveButton.grid(row=6, column=0, columnspan=2, padx=5, pady=30)

# Application icon
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.config(background="lightgrey")

# Application main loop
root.mainloop()
