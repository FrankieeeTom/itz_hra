from pyray import *
from time import *

# Initialize window
init_window(800, 600, "Frame Delay Example")

target_fps = 60
delay_between_frames = 0.5  # 0.5 seconds
last_update_time = time.perf_counter()

while not window_should_close():
    current_time = time.perf_counter()
    
    # Update only after the delay has passed
    if current_time - last_update_time >= delay_between_frames:
        last_update_time = current_time
        print("Frame updated")  # Your update logic here
    
    # Render
    begin_drawing()
    clear_background(RAYWHITE)
    draw_text("Waiting...", 350, 280, 20, DARKGRAY)
    end_drawing()

close_window()
