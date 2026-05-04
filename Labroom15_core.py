import cv2
import re
import easyocr

reader = easyocr.Reader(['en']) 

def super_refine_car(raw_txt): 
    s = "".join([c for c in raw_txt if c.isalnum()]).upper() 
    if len(s) < 7: return s
    chars = list(s) 
    
    chu_sang_so = {
        'S': '5', 'E': '5', 'O': '0', 'D': '0', 
        'I': '1', 'Z': '2', 'G': '6', 'T': '7', 'B': '8', 'A': '4'
    }
    so_sang_chu = {
        '4': 'A', '0': 'D', '1': 'I', '5': 'S', 
        '8': 'B', '6': 'E', '2': 'Z', '3': 'A'
    }

    for i in range(2): 
        if not chars[i].isdigit():
            chars[i] = chu_sang_so.get(chars[i], '0')

    if chars[2].isdigit(): 
        chars[2] = so_sang_chu.get(chars[2], 'A') 
    
    for i in range(3, len(chars)): 
        if not chars[i].isdigit():
            chars[i] = chu_sang_so.get(chars[i], chars[i])
        if not chars[i].isdigit(): chars[i] = '0'
            
    return "".join(chars) 

def process_image(path): 
    img = cv2.imread(path) 
    if img is None: return None 
    results = reader.readtext(img) 
    raw_list = [re.sub(r'[^0-9A-Z]', '', x[1].upper()) for x in results] 
    target_plate = "" 
   
    for i, fragment in enumerate(raw_list): 
        if len(fragment) >= 3: 
            match = re.search(r'^[0-9SEOD]{2}[A-Z43]', fragment) 
            if match:
                if len(fragment) <= 4: 
                    target_plate = fragment 
                    for j in range(i + 1, min(i + 3, len(raw_list))):
                        if any(c.isdigit() for c in raw_list[j]):
                            target_plate += raw_list[j] 
                else:
                    target_plate = fragment 
                break 
 
    if target_plate: 
        refined = super_refine_car(target_plate)
        final = refined[:8]
        prefix, nums = final[:3], final[3:]
        if len(nums) == 5:
            return f"{prefix}-{nums[:3]}.{nums[3:]}" 
        else:
            return f"{prefix}-{nums}" 
    return None 
