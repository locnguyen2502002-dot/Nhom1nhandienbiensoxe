import cv2
import numpy as np
import easyocr
import re
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Khởi tạo EasyOCR
reader = easyocr.Reader(['en'])

def clean_txt(text):
    return re.sub(r'[^0-9A-Z]', '', text.upper())

def apply_filters(img_path):
    """Tạo ra các phiên bản ảnh khác nhau để OCR thử vận may"""
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    versions = []
    # 1. Ảnh gốc (Cho biển trắng/vàng)
    versions.append(gray)
    
    # 3. Ảnh tăng độ tương phản mạnh (Thresholding)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    versions.append(thresh)

    return versions

def detect_plate(path):
    result_label.config(text="Đang quét đa hệ...", fg="orange")
    root.update()

    processed_versions = apply_filters(path)
    final_plate = ""

    for i, img_ver in enumerate(processed_versions):
        # Lưu ảnh tạm để EasyOCR đọc
        tmp_file = f"temp_ver_{i}.jpg"
        cv2.imwrite(tmp_file, img_ver)
        
        results = reader.readtext(tmp_file)
        raw_blocks = [clean_txt(res[1]) for res in results]
        
        print(f"Thử bộ lọc {i}: {raw_blocks}")

        # Ghép và tìm mã tỉnh (2 số + 1 chữ)
        full_text = "".join(raw_blocks)
        match = re.search(r'\d{2}[A-Z]', full_text)
        
        if match:
            start = match.start()
            # Cắt đúng 8 ký tự cho biển 5 số (XXY-123.45)
            # Hoặc 7 ký tự cho biển 4 số
            candidate = full_text[start:start+8]
            
            if len(candidate) >= 7:
                # Định dạng lại đầu ra
                p1 = candidate[:3]
                nums = candidate[3:]
                if len(nums) > 5: nums = nums[:5] # Cắt rác thừa
                
                final_plate = f"{p1}-{nums[:3]}.{nums[3:]}" if len(nums)==5 else f"{p1}-{nums}"
                break 

    if final_plate:
        result_label.config(text=f"Biển số: {final_plate}", fg="blue")
    else:
        result_label.config(text="Không tìm thấy biển", fg="red")

# --- GIAO DIỆN GUI (Giữ nguyên cấu trúc bạn đang dùng) ---
def open_image():
    global image_path
    image_path = filedialog.askopenfilename()
    if not image_path: return
    img = Image.open(image_path).resize((400, 250))
    img_tk = ImageTk.PhotoImage(img)
    panel.config(image=img_tk); panel.image = img_tk

root = tk.Tk(); root.title("OCR Đa Hệ Biển Số"); root.geometry("500x600")
tk.Button(root, text="CHỌN ẢNH", command=open_image).pack(pady=10)
tk.Button(root, text="ĐỌC BIỂN SỐ", command=lambda: detect_plate(image_path), bg="#2ecc71", fg="white").pack(pady=5)
panel = tk.Label(root, bg="gray"); panel.pack(pady=10)
result_label = tk.Label(root, text="KẾT QUẢ", font=("Arial", 20, "bold")); result_label.pack(pady=20)
root.mainloop()