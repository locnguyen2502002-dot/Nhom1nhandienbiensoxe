import cv2
import re
import easyocr

# Khởi tạo OCR một lần duy nhất để tiết kiệm tài nguyên
reader = easyocr.Reader(['en']) # có khả năng quét và nhận diện văn bản từ hình ảnh.ngôn ngữ đọc là TA

def super_refine_car(raw_txt): 
    # Làm sạch: Chỉ giữ chữ và số 
    s = "".join([c for c in raw_txt if c.isalnum()]).upper() #Chuyển chữ thường thành chữ hoa,raw_txt ocr đọc bs cắt thành chuỗi,s là ktra số chữ
    if len(s) < 7: return s # Nếu độ dài nhỏ hơn 7 thì trả về s
    
    chars = list(s) #Chuyển thành list
    
    # BẢNG DỊCH TỔNG LỰC: Ưu tiên S, E -> 5 | O, D -> 0 # chu_sang_so là bảng chuyển chữ sang số
    chu_sang_so = {
        'S': '5', 'E': '5', 'O': '0', 'D': '0', 
        'I': '1', 'Z': '2', 'G': '6', 'T': '7', 'B': '8', 'A': '4'
    }
    so_sang_chu = {
        '4': 'A', '0': 'D', '1': 'I', '5': 'S', 
        '8': 'B', '6': 'E', '2': 'Z', '3': 'A'
    }

    # --- BƯỚC 1: 2 VỊ TRÍ ĐẦU PHẢI LÀ SỐ (ÉP S, E THÀNH 5) ---
    for i in range(2): # bỏ 2 vị trí đầu tiên xử lý từ vị trí thứ 2
        if not chars[i].isdigit(): # Nếu không phải số
            chars[i] = chu_sang_so.get(chars[i], '0') # Chuyển chữ thành số

    # --- BƯỚC 2: VỊ TRÍ THỨ 3 PHẢI LÀ CHỮ ---
    if chars[2].isdigit(): # Nếu vị trí thứ 3 là số
        chars[2] = so_sang_chu.get(chars[2], 'A') # Chuyển số thành chữ
    
    # --- BƯỚC 3: TẤT CẢ CÁC VỊ TRÍ CÒN LẠI PHẢI LÀ SỐ ---
    for i in range(3, len(chars)): # Bỏ qua 3 kí tự đầu tiên xử lý từ vị trí thứ 3 trở đi
        if not chars[i].isdigit(): # Ktra coi có phải số hay không
            chars[i] = chu_sang_so.get(chars[i], chars[i]) # Nếu tìm thấy thì chuyển thành số,không tìm thấy thì giữ nguyên
        if not chars[i].isdigit(): chars[i] = '0' # Này thì là chốt chặn đảm bảo từ vị trí thứ 3 trở đi đều là số
            
    return "".join(chars) # Trả về chuỗi ghép các chuỗi lại(các chuỗi này đã được xử lý)

def process_image(path): # Xử lý ảnh
    img = cv2.imread(path) # Đọc ảnh từ đường dẫn sau đó biến ảnh đó thành ma trận
    if img is None: return None # Nếu ảnh không đọc được thì trả về None
    
    results = reader.readtext(img) # Đọc chữ trong ảnh
    
    # Lấy các mảnh, xóa rác, viết hoa
    raw_list = [re.sub(r'[^0-9A-Z]', '', x[1].upper()) for x in results] # Xóa ký tự không phải số và chữ,for x in results lặp các phần tử trong results
    
    target_plate = "" # Biến lưu plate

    # Duyệt để tìm mã tỉnh 
    for i, fragment in enumerate(raw_list): # Lặp qua từng phần tử trong raw_list đồng thời lấy luôn vị trí của nó(index,values)
        # Chấp nhận cả mảnh bắt đầu bằng S hoặc E
        if len(fragment) >= 3: # Nếu mảnh có độ dài >= 3
            # Regex chấp nhận ký tự đầu là Số hoặc S, E, O, D
            match = re.search(r'^[0-9SEOD]{2}[A-Z43]', fragment) # Regex để tìm mã tỉnh
            if match:
                if len(fragment) <= 4: # Nếu mảnh có độ dài <= 4
                    target_plate = fragment # Gán mảnh vào target_plate
                    # Tìm và ghép mảnh số đứng ngay sau
                    for j in range(i + 1, min(i + 3, len(raw_list))): # Lặp đến hết hoặc đến 3 mảnh sau
                        if any(c.isdigit() for c in raw_list[j]): # Nếu mảnh có chứa số
                            target_plate += raw_list[j] # Ghép mảnh số vào
                else:
                    target_plate = fragment # Gán mảnh vào target_plate
                break # Dừng lại khi tìm thấy mã tỉnh
 
    if target_plate: # Nếu tìm thấy plate
        # Đưa vào xưởng nắn lại kiểu chữ
        refined = super_refine_car(target_plate) # Nắn lại kiểu chữ
        final = refined[:8] # Lấy 8 ký tự đầu
        
        prefix, nums = final[:3], final[3:] # Tách prefix và nums (prefix là 3 ký tự đầu, nums là  ký tự sau)
        
        if len(nums) == 5: # Nếu nums có 5 ký tự
            return f"{prefix}-{nums[:3]}.{nums[3:]}" # Trả về định dạng
        else:
            return f"{prefix}-{nums}" # Trả về định dạng
            
    return None # Nếu không tìm thấy platej