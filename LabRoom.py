import tkinter as tk 
import os
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

def bogoc(image_path, size, radius):
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + size, radius, fill=255)
    bg_color = "darkgray" 
    output = Image.new("RGBA", size, bg_color) 
    output.paste(img, (0, 0), mask=mask)
    return output.convert("RGB")

n=tk.Tk()
n.title("ALPR System")
n.geometry("1920x1080")
n.configure(bg="white")

b = os.path.dirname(os.path.abspath(__file__))
logo = os.path.join(b, "logoicon.ico")
hinhnutupload = os.path.join(b, "upload_button.jpg")
n.iconbitmap(logo)

tk.Label(n, text="PLATE RECOGNITION", font=("Lucida Console", 50, "bold")).place(x=80, y=60)

khung = tk.Frame(n, bg="darkgray", highlightthickness=0,bd=0)
khung.place(relx=0.4, rely=0.55, width=800, height=500, anchor="center")

def open_file():
    a = filedialog.askopenfilename(
        title="Chọn ảnh",
        filetypes=[("Image files", "*.png *.jpg")]
    )
    if a:
        hinhanh = Image.open(a)
        hinhanh = hinhanh.resize((800,500),Image.Resampling.LANCZOS)

        anhtk = ImageTk.PhotoImage(hinhanh)
        
        hienthianh = tk.Label(khung, image=anhtk, bg="darkgray", bd=0)
        hienthianh.image = anhtk
        hienthianh.place(relx=0.5, rely=0.5, anchor="center")
        nutUpload.place_forget()

kichthuocnut = (100, 100)
dobogoc = 20
hinhdabogoc = bogoc(hinhnutupload, kichthuocnut, dobogoc)
hinhnuttailen = ImageTk.PhotoImage(hinhdabogoc)

nutUpload = tk.Button(
    khung, 
    image=hinhnuttailen,
    command = open_file,
    font=("Arial",12,"bold"),
    bg="darkgray",
    relief="flat",
    bd=0,
    highlightthickness=0,
    cursor="hand2"
)
nutUpload.image = hinhnuttailen
nutUpload.place(relx=0.5, rely=0.5, anchor="center")

nutthem = tk.Button(n, text=" + ", command = open_file, font=("Arial", 35, "bold"),relief="flat", width=5,cursor="hand2")
nutthem.place(x=1100, y=200)

nutchay = tk.Button(n, text= "▶", font=("Arial", 35, "bold"), width=5, fg="green",relief="flat",cursor="hand2")
nutchay.place(x=1100, y=320)

tieudeKQ = tk.Label(n, text="Plate read: ", font=("Lucida Console", 11), bg="white")
tieudeKQ.place(x=1100, y=460)

khungKQ = tk.Text(
    n,
    bd=2,
    relief="solid",
    bg="white",
    font=("Consolas", 20, "bold"),
    width=13,
    height=2
)
khungKQ.place(x=1100, y=490, width=350, height=150)

nutcopy = tk.Button(n,text="📄",font=("Arial", 15),relief="flat",cursor="hand2")
nutcopy.place(x=1410, y=650)

nutcrop = tk.Button(n, text="✂️", font=("Arial",30), width=5, height=2,relief="flat", cursor="hand2")
nutcrop.place(x=40, y=350)

nutls = tk.Button(n, text="🕑", font=("Arial",30), width=5, height=2,relief="flat", cursor="hand2")
nutls.place(x=40, y=500)

n.mainloop()