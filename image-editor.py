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
global edited_image, crop_rectangle, start_x, start_y, end_x, end_y, img_display, history
start_x = start_y = end_x = end_y = None
crop_rectangle = None
history = []  # History of image states

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#Filter edits
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

def saveImage():
    global edited_image
    if edited_image:
        edited_image.save("copy.jpg", "JPEG")

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename

#Resize based on give size
def resize_image(img, max_width, max_height):
    width_ratio = max_width / img.width
    height_ratio = max_height / img.height
    ratio = min(width_ratio, height_ratio)
    new_width = int(img.width * ratio)
    new_height = int(img.height * ratio)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

#Opening file from local storage
def open_img():
    global imagePath, edited_image, img_display, history
    x = openfn()
    imagePath = x
    img = Image.open(x)

    max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()

    img = resize_image(img, max_width, max_height)
    img_display = ImageTk.PhotoImage(img)
    
    canvas.create_image(0, 0, anchor="nw", image=img_display)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    # Save the original image for editing
    edited_image = Image.open(imagePath)
    history.clear()  #Clear history when a new image is opened
    history.append(edited_image.copy())  #Save the original image to history

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
    global edited_image, start_x, start_y, end_x, end_y, history, img_display, crop_rectangle
    if edited_image:
        if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
            #Save the current image to history before cropping
            history.append(edited_image.copy())

            image_width, image_height = edited_image.size

            canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
            scale_x = image_width / canvas_width
            scale_y = image_height / canvas_height

            img_start_x = int(start_x * scale_x)
            img_start_y = int(start_y * scale_y)
            img_end_x = int(end_x * scale_x)
            img_end_y = int(end_y * scale_y)

            cropped_image = edited_image.crop((img_start_x, img_start_y, img_end_x, img_end_y))
            edited_image = cropped_image

            start_x = start_y = end_x = end_y = None

            if crop_rectangle is not None:
                canvas.delete(crop_rectangle)
                crop_rectangle = None

            #Update the displayed image
            max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
            cropped_image = resize_image(cropped_image, max_width, max_height)
            img_display = ImageTk.PhotoImage(cropped_image)

            canvas.create_image(0, 0, anchor="nw", image=img_display)
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
        else:
            print("Crop area not defined. Please draw a crop rectangle first.")


# Undo the last crop operation
def undo_crop(event=None):
    global edited_image, history, img_display, crop_rectangle
    if len(history) > 1:
        history.pop()
        edited_image = history[-1]  # Revert to the previous image

        start_x = start_y = end_x = end_y = None
        if crop_rectangle is not None:
            canvas.delete(crop_rectangle) 
            crop_rectangle = None

        # Update the displayed image
        max_width, max_height = rightFrame.winfo_width(), rightFrame.winfo_height()
        img_to_display = resize_image(edited_image, max_width, max_height)
        img_display = ImageTk.PhotoImage(img_to_display)

        canvas.create_image(0, 0, anchor="nw", image=img_display)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
    else:
        print("No more actions to undo.")

#Menu button for file opening
fileBttn = ttk.Menubutton(frame, text="File")
Menu1 = ttk.Menu(fileBttn, tearoff=0)
Menu1.add_command(label="Open file", command=open_img)
fileBttn["menu"] = Menu1
fileBttn.pack(padx=10, pady=10)

#Left side option bar for picking an option to edit image
leftFrame = tk.Frame(root)
leftFrame.pack(side="left", fill=tk.Y)
pickedOption = tk.StringVar()
RadioButton = ttk.Radiobutton(leftFrame, text="Greyscale", variable=pickedOption, value="Greyscale")
RadioButton.grid(row=0, column=0,columnspan=2,padx=5,pady=5)
applyButton = ttk.Button(leftFrame, text="Apply", command=editImage)
applyButton.grid(row=1, column=0,columnspan=2,padx=5,pady=5)

#Crop Button
cropButton = ttk.Button(leftFrame, text="Crop", command=crop_image)
cropButton.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

saveButton = ttk.Button(leftFrame, text="Save Copy", command=saveImage)
saveButton.grid(row=3, column=0, columnspan=2, padx=5, pady=30)

#Canvas for cropping
canvas = tk.Canvas(rightFrame, bg='white')
canvas.pack(fill="both", expand=True)

#cropping binds
canvas.bind("<ButtonPress-1>", start_crop)
canvas.bind("<B1-Motion>", draw_crop_rectangle)

root.bind("<Control-z>", undo_crop)

icon = tk.PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.config(background="lightgrey")

# Application main loop
root.mainloop()
