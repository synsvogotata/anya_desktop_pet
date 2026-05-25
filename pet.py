import tkinter as tk
import random
from PIL import Image, ImageTk, ImageDraw

class DesktopPet:
    def __init__(self, image_path):
        self.root = tk.Tk()
        
        # Налаштування прозорості та відображення поверх усіх вікон
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black') # Чорний колір стане прозорим (для Windows)
        
        # Завантаження спрайт-листа
        self.img = Image.open(image_path)
        self.img_w, self.img_h = self.img.size
        
        # Наше зображення має сітку: 2 рядки та 10 колонок
import tkinter as tk
import random
import os
import sys
from PIL import Image, ImageTk, ImageDraw

# Функція, яка дозволяє вшити картинку всередину .exe файла
def resource_path(relative_path):
    try:
        # PyInstaller створює тимчасову папку _MEIPASS при запуску .exe
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DesktopPet:
    def __init__(self, image_name):
        self.root = tk.Tk()
        
        # Налаштування вікна (поверх усіх вікон, без рамок, прозоре тло)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black')
        
        # Завантажуємо картинку через наш магічний шлях resource_path
        image_path = resource_path(image_name)
        self.img = Image.open(image_path)
        self.img_w, self.img_h = self.img.size
        
        self.cols = 10
        self.rows = 2
        self.frame_w = self.img_w // self.cols
        self.frame_h = self.img_h // self.rows
        
        # Затираємо текст зверху
        draw = ImageDraw.Draw(self.img)
        draw.rectangle([0, 0, self.img_w, int(self.frame_h * 0.22)], fill="black")
        
        self.sprites = {"idle": [], "walk_right": [], "walk_left": []}
        self.load_sprites()
        
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.x = random.randint(0, self.screen_w - self.frame_w)
        self.y = self.screen_h - self.frame_h - 60 
        
        self.label = tk.Label(self.root, bd=0, bg='black')
        self.label.pack()
        
        self.state = "idle"
        self.frame_idx = 0
        self.action_timer = 0
        
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        
        self.update()
        self.root.mainloop()
        
    def load_sprites(self):
        def get_frame(r, c):
            left = c * self.frame_w
            top = r * self.frame_h
            right = left + self.frame_w
            bottom = top + self.frame_h
            cropped = self.img.crop((left, top, right, bottom))
            return ImageTk.PhotoImage(cropped)
        
        self.sprites["idle"].append(get_frame(0, 0))
        
        for r in range(2):
            for c in [2, 3, 4]:
                self.sprites["walk_right"].append(get_frame(r, c))
                
        for r in range(2):
            for c in [6, 7, 8, 9]:
                self.sprites["walk_left"].append(get_frame(r, c))

    def update(self):
        self.action_timer -= 1
        if self.action_timer <= 0:
            self.state = random.choice(["idle", "walk_left", "walk_right"])
            self.action_timer = random.randint(40, 120)
            self.frame_idx = 0
            
        if self.state == "idle":
            frames = self.sprites["idle"]
            self.frame_idx = self.frame_idx % len(frames)
            current_frame = frames[self.frame_idx]
            
        elif self.state == "walk_left":
            frames = self.sprites["walk_left"]
            self.frame_idx = (self.frame_idx + 1) % len(frames)
            current_frame = frames[self.frame_idx]
            self.x -= 4
            if self.x < 0:
                self.x = 0
                self.state = "walk_right"
                
        elif self.state == "walk_right":
            frames = self.sprites["walk_right"]
            self.frame_idx = (self.frame_idx + 1) % len(frames)
            current_frame = frames[self.frame_idx]
            self.x += 4
            if self.x > self.screen_w - self.frame_w:
                self.x = self.screen_w - self.frame_w
                self.state = "walk_left"
        
        self.label.config(image=current_frame)
        self.root.geometry(f"{self.frame_w}x{self.frame_h}+{self.x}+{self.y}")
        self.root.after(120, self.update)

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def drag(self, event):
        self.x = self.root.winfo_x() + event.x - self.drag_x
        self.y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{self.x}+{self.y}")

if __name__ == "__main__":
    # Назва файлу картинки, який ми будемо вшивати
    DesktopPet("anya_sprites.jpg")
