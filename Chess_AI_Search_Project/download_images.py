import urllib.request
import os

# Tạo thư mục images nếu chưa có
os.makedirs("images", exist_ok=True)

# Danh sách tên file chữ thường
pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']

print("Đang tải bộ ảnh quân cờ từ máy chủ dự phòng...")

for p in pieces:
    # Lấy ảnh từ nguồn ổn định (Theme 'neo' rất đẹp và rõ nét)
    url = f"https://images.chesscomfiles.com/chess-themes/pieces/neo/150/{p}.png"
    filename = f"images/{p}.png"
    
    try:
        # Thêm Header User-Agent để máy chủ không tưởng lầm đây là bot tấn công
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f" [OK] Đã tải thành công: {filename}")
    except Exception as e:
        print(f" [LỖI] Không thể tải {p}: {e}")

print("\nHoàn tất! Bây giờ bạn có thể chạy lại file gui.py.")