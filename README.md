# ♟️ Machine Learning-Based Chess Engine

Đây là mã nguồn dự án **Trí tuệ Nhân tạo chơi Cờ vua (Chess AI)**, thuộc khuôn khổ Bài tập lớn (Assignment) môn **Nhập môn Trí tuệ nhân tạo (CO3061)** - Đại học Bách Khoa TP.HCM (HCMUT).

Dự án tập trung vào việc xây dựng Agent chơi cờ dựa trên các phương pháp **Machine Learning**, đồng thời phát triển một Agent dựa trên **Thuật toán Tìm kiếm (Search Algorithm)** để đối chiếu và đánh giá hiệu năng.

## 🌟 Các tính năng chính (Features)

* **Giao diện đồ họa (UI):** Tích hợp Pygame mang lại trải nghiệm tương tác trực quan (người chơi có thể đấu trực tiếp với máy).
* **Machine Learning Agent:** Tác tử chính của dự án, được huấn luyện để đưa ra các nước đi thông minh thông qua nhận diện thế trận.
* **Search-based Agent (Đối trọng):** Tác tử sử dụng thuật toán Minimax kết hợp cắt tỉa Alpha-Beta (Alpha-Beta Pruning) và hàm lượng giá (Piece-Square Tables).
* **Chế độ kiểm thử (Evaluation Mode):** Tự động cho ML Agent đấu với Random Agent (đảm bảo tỷ lệ thắng tuyệt đối 10/10) hoặc đấu với Human.

## 📂 Cấu trúc thư mục (Project Structure)

* `main_ui.py`: File khởi chạy chính, chứa logic Giao diện người dùng (Pygame).
* `agent.py`: Chứa định nghĩa và logic dự đoán của Machine Learning Agent và Random Agent.
* `engine.py` / `evaluation.py`: Chứa thuật toán tìm kiếm truyền thống (Minimax) và hàm lượng giá để đối chiếu.
* `download_assets.py`: Script tự động tải bộ hình ảnh quân cờ chuẩn.
* `assets/`: Thư mục chứa hình ảnh quân cờ (sẽ tự động tạo ra khi chạy script).
* `saved_models/`: Nơi lưu trữ các file mô hình Machine Learning đã được huấn luyện (`.pth`, `.h5`).

## ⚙️ Cài đặt và Chạy thử nghiệm

**Bước 1: Tải mã nguồn về máy**
```bash
git clone [https://github.com/chefQuang/Machine-Learning-Based-Chess-Engine.git](https://github.com/chefQuang/Machine-Learning-Based-Chess-Engine.git)
cd Machine-Learning-Based-Chess-Engine
****Bước 2: Cài đặt thư viện
pip install pygame chess
******** Để chạy trò chơi
python main_ui.py
