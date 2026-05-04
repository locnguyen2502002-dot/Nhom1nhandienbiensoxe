import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import Labroom15_core as engine


def ui_detect():
    if not image_path:
        messagebox.showwarning("Lỗi", "Vui lòng chọn ảnh")
        return
    
    khungKQ.delete("1.0", tk.END)
    khungKQ.insert(tk.END, "Đang đọc...")
    root.update()

    plate = engine.process_image(image_path)

    khungKQ.delete("1.0", tk.END) 
    if plate:
        khungKQ.insert(tk.END, plate) 
    else:
        khungKQ.insert(tk.END, "Không tìm thấy!")

def open_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not image_path: return
    
    img = Image.open(image_path)
    img.thumbnail((800,500)) 
    img_tk = ImageTk.PhotoImage(img)
    khung.config(image=img_tk)
    khung.image = img_tk

#KHU VỰC THIẾT KẾ GIAO DIỆN
root = tk.Tk()
root.title("ALPR System")
root.geometry("1920x1080")
root.configure(bg="white")

image_path = ""

# Tiêu đề
header =tk.Label(root, text="NHẬN DIỆN BIỂN SỐ XE", font=("Cascadia Code", 50, "bold"), fg="blue", bg="white").place(x=80, y=60)

# Nút chọn ảnh
nuttal=tk.Button(root, text="+", command=open_image, font=("Cascadia Code", 35, "bold"),relief="flat", bg="blue", fg="white", width=5,cursor="hand2")
nuttal.place(x=1100, y=200)

nutdoc=tk.Button(root, text="Đọc", command=ui_detect, bg="blue", fg="white", font=("Cascadia Code", 35, "bold"), width=5,relief="flat",cursor="hand2")
nutdoc.place(x=1100, y=320)

# Khung hiển thị ảnh
khung = tk.Label(root, bg="lightgray", bd=0, relief="sunken", highlightthickness=0)
khung.place(relx=0.4, rely=0.55, width=800, height=500, anchor="center")

# Khung hiển thị kết quả
tieudeKQ = tk.Label(root, text="Kết quả: ", font=("Cascadia Code", 11), bg="white")
tieudeKQ.place(x=1100, y=460)
khungKQ = tk.Text(root,bd=1,relief="solid",bg="white",font=("Consolas", 30, "bold"),width=13,height=2)
khungKQ.place(x=1100, y=490, width=350, height=150)

root.mainloop()
