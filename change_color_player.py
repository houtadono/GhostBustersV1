from PIL import Image
import os

# Đường dẫn đến thư mục chứa các tệp hình ảnh
image_dir = f'./Assets/Player/'

# Lặp qua tất cả các tệp hình ảnh trong thư mục
for filename in os.listdir(image_dir):
    # Kiểm tra xem tệp có định dạng hình ảnh (jpg, png, gif, ...) không
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'):
        # Mở tệp hình ảnh và chuyển sang chế độ RGB
        image = Image.open(image_dir + filename)
        # Lặp qua tất cả các pixel trong hình ảnh
        for x in range(image.width):
            for y in range(image.height):
                # Nếu pixel hiện tại là màu trắng (255, 255, 255)
                print(image.getpixel((x, y)))
                if image.getpixel((x, y)) == (255, 255, 255, 255):
                    # Thay đổi màu của pixel thành màu đỏ (255, 0, 0)
                    image.putpixel((x, y), (201, 60, 36,255))
        # Lưu hình ảnh mới vào cùng đường dẫn và tên tệp hình ảnh cũ
        image.save(f'./Assets/AdminRed/' + filename)