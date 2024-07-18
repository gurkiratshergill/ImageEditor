import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog

imagePath = ''

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def openFile():
    pass

def editImage():
    global imagePath
    if imagePath:
        with Image.open(imagePath) as img:
            blackAndWhite = img.convert('L')
            max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
            blackAndWhite = resize_image(blackAndWhite, max_width, max_height)
            blackAndWhite = ImageTk.PhotoImage(blackAndWhite)
        clear_frame(rightFrame)
        panel = tk.Label(rightFrame, image=blackAndWhite)
        panel.image = blackAndWhite
        panel.pack()

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

    # Get the application window size
    max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()

    # Resize the image to fit within the application window size
    img = resize_image(img, max_width, max_height)
    img = ImageTk.PhotoImage(img)
    clear_frame(rightFrame)
    panel = tk.Label(rightFrame, image=img)
    panel.image = img
    panel.pack()

# Main Window
root = tk.Tk()
root.geometry("800x600")  # Set a larger window size to accommodate images
root.title("Image Editor")
frame = tk.Frame(root)
frame.pack(side="top", fill=tk.X)
rightFrame = tk.Frame(root)
rightFrame.pack(side="right", padx=10, pady=10, expand=True, fill=tk.BOTH)

# Menu button for file opening
fileBttn = tk.Menubutton(frame, text="File", bg="white")
Menu1 = tk.Menu(fileBttn, tearoff=0)
Menu1.add_command(label="Open file", command=open_img)
fileBttn["menu"] = Menu1
fileBttn.pack(padx=10, pady=10)

# Left side option bar for picking an option to edit image
leftFrame = tk.Frame(root)
leftFrame.pack(side="left", fill=tk.Y)
pickedOption = tk.StringVar()
RadioButton = tk.Radiobutton(leftFrame, text="Black & White", variable=pickedOption)
RadioButton.pack(padx=5, pady=5)
applyButton = tk.Button(leftFrame, text="Apply", command=editImage, bg="white")
applyButton.pack(padx=5, pady=5)

saveButton = tk.Button(leftFrame, text="Save Copy", bg="white")
saveButton.pack(padx=10, pady=10)

# Application icon
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.config(background="lightgrey")

# Application main loop
root.mainloop()

