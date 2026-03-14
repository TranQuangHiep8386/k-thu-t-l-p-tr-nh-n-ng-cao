# Báo Cáo: Xây Dựng Chương Trình Quản Lý Lịch Cá Nhân

## 1. Giới Thiệu
Trong cuộc sống hiện đại, việc quản lý thời gian hiệu quả là vô cùng quan trọng. Chương trình quản lý lịch cá nhân được xây dựng nhằm hỗ trợ người dùng tạo, lưu trữ và theo dõi các sự kiện, công việc hàng ngày một cách trực quan và khoa học. Đề tài này tập trung vào việc áp dụng các cấu trúc dữ liệu và giải thuật cơ bản để giải quyết bài toán quản lý thông tin thời gian thực.

## 2. Cơ Sở Lý Thuyết

### 2.1. Phân Tích Bài Toán
Bài toán yêu cầu xây dựng một ứng dụng có khả năng:
*   **Lưu trữ sự kiện**: Mỗi sự kiện cần có ngày, giờ, tiêu đề và mô tả.
*   **Thêm/Sửa/Xóa (CRUD)**: Người dùng có thể thao tác với dữ liệu sự kiện.
*   **Hiển thị**: Hiển thị lịch theo tháng và danh sách sự kiện theo ngày được chọn.
*   **Lưu trữ lâu dài**: Dữ liệu không bị mất khi tắt chương trình.

### 2.2. Cấu Trúc Dữ Liệu
Để quản lý dữ liệu hiệu quả, chúng ta sử dụng các cấu trúc dữ liệu sau:

1.  **Lớp Sự kiện (Class Event)**:
    *   Đại diện cho một sự kiện đơn lẻ.
    *   Thuộc tính: `id` (định danh duy nhất), `date` (ngày), `time` (giờ), `title` (tiêu đề), `description` (mô tả).
    *   Lý do: Giúp đóng gói dữ liệu gọn gàng (OOP).

2.  **Bảng băm (Hash Map / Dictionary)**:
    *   Cấu trúc: `Dictionary<String, List<Event>>`
    *   Key: Chuỗi ngày định dạng "YYYY-MM-DD".
    *   Value: Danh sách các đối tượng `Event` diễn ra trong ngày đó.
    *   Lý do: Cho phép truy xuất nhanh danh sách sự kiện của một ngày bất kỳ với độ phức tạp trung bình là O(1).

3.  **Danh sách (List/Array)**:
    *   Dùng để lưu trữ các sự kiện trong cùng một ngày.
    *   Lý do: Số lượng sự kiện trong một ngày thường nhỏ, việc duyệt và thao tác trên danh sách là đơn giản và hiệu quả.

### 2.3. Giải Thuật

#### 2.3.1. Thêm sự kiện & Sắp xếp
Khi thêm một sự kiện mới vào một ngày:
1.  Truy xuất danh sách sự kiện của ngày đó từ Dictionary.
2.  Thêm sự kiện vào cuối danh sách.
3.  **Sắp xếp lại danh sách** theo thời gian (giờ) để hiển thị theo trình tự thời gian.
    *   Thuật toán sắp xếp: Timsort (thuật toán mặc định của Python `sort()`).

#### 2.3.2. Tìm kiếm / Truy xuất
*   Để lấy sự kiện của một ngày: Sử dụng Key (ngày) để tra cứu trong Dictionary.

#### 2.3.3. Xóa sự kiện
*   Duyệt qua danh sách sự kiện của ngày tương ứng.
*   Tìm sự kiện có `id` trùng khớp và loại bỏ nó khỏi danh sách.

## 3. Đánh Giá Độ Phức Tạp

Giả sử:
*   $N$: Tổng số ngày có sự kiện.
*   $M$: Số lượng sự kiện trung bình trong một ngày (thường là số nhỏ, $M < 50$).

### 3.1. Độ phức tạp Thời gian (Time Complexity)
*   **Truy xuất sự kiện theo ngày**: $O(1)$ trung bình (do dùng Hash Map).
*   **Thêm sự kiện**:
    *   Tra cứu ngày: $O(1)$.
    *   Thêm vào list: $O(1)$.
    *   Sắp xếp lại list kích thước $M$: $O(M \log M)$.
    *   Tổng: $O(M \log M)$. Vì $M$ nhỏ nên thao tác này gần như tức thời.
*   **Xóa sự kiện**:
    *   Tìm kiếm trong list kích thước $M$: $O(M)$.
    *   Xóa phần tử: $O(M)$.
    *   Tổng: $O(M)$.

### 3.2. Độ phức tạp Không gian (Space Complexity)
*   $O(Total\_Events)$: Cần bộ nhớ để lưu trữ toàn bộ các đối tượng sự kiện. Với ứng dụng cá nhân, dung lượng này là không đáng kể.

## 4. Kết Luận
Việc kết hợp Dictionary để tra cứu nhanh theo ngày và List được sắp xếp để quản lý sự kiện trong ngày là giải pháp tối ưu cho bài toán này. Nó cân bằng giữa tốc độ truy xuất và sự đơn giản trong cài đặt, đáp ứng tốt yêu cầu về hiệu năng cho bài toán quản lý lịch cá nhân.
