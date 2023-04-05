import pygame
import pygame_gui

pygame.init()

# Thiết lập cửa sổ Pygame
win_width, win_height = 640, 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dialog example")

# Tạo bộ quản lý GUI
ui_manager = pygame_gui.UIManager((win_width, win_height))

# Tạo widget nút "Yes"
btn_yes = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((win_width/2-60, win_height/2-10), (50, 20)),
    text="Yes",
    manager=ui_manager
)

# Tạo widget nút "No"
btn_no = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((win_width/2+10, win_height/2-10), (50, 20)),
    text="No",
    manager=ui_manager
)

# Vòng lặp game
running = True
while running:
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Xử lý sự kiện cho widget GUI
        ui_manager.process_events(event)

    # Cập nhật trạng thái các widget GUI
    ui_manager.update(pygame.time.Clock().tick(60)/1000.0)

    # Vẽ các widget GUI
    win.fill((255, 255, 255))
    ui_manager.draw_ui(win)

    pygame.display.update()

pygame.quit()
