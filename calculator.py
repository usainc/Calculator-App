import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hesap Makinesi - by @UsainC")
        self.root.configure(bg='#1c1c1c')
        
        # Pencere boyutunu sabitle
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Değişkenler
        self.memory = 0
        self.history = []
        self.is_scientific = False
        self.current_operation = None
        self.last_number = None
        self.new_number = True
        self.buttons_frame = None  # buttons_frame'i sınıf değişkeni olarak tanımla
        
        # Tüm temalar
        self.themes = {
            "dark": {
                "name": "Koyu Tema",
                "bg": "#1c1c1c",
                "display_bg": "#1c1c1c",
                "display_fg": "#ffffff",
                "num_button": "#333333",
                "num_button_hover": "#737373",
                "op_button": "#ff9f0a",
                "op_button_hover": "#ffc158",
                "func_button": "#a5a5a5",
                "func_button_hover": "#d4d4d4",
                "text_color": "white",
            },
            "light": {
                "name": "Açık Tema",
                "bg": "#f0f0f0",
                "display_bg": "#f0f0f0",
                "display_fg": "#000000",
                "num_button": "#ffffff",
                "num_button_hover": "#e6e6e6",
                "op_button": "#ff9f0a",
                "op_button_hover": "#ffc158",
                "func_button": "#d4d4d4",
                "func_button_hover": "#b9b9b9",
                "text_color": "black",
            },
            "blue": {
                "name": "Mavi Tema",
                "bg": "#1a237e",
                "display_bg": "#1a237e",
                "display_fg": "#ffffff",
                "num_button": "#283593",
                "num_button_hover": "#3949ab",
                "op_button": "#5c6bc0",
                "op_button_hover": "#7986cb",
                "func_button": "#3f51b5",
                "func_button_hover": "#5c6bc0",
                "text_color": "white",
            },
            "purple": {
                "name": "Mor Tema",
                "bg": "#4a148c",
                "display_bg": "#4a148c",
                "display_fg": "#ffffff",
                "num_button": "#6a1b9a",
                "num_button_hover": "#7b1fa2",
                "op_button": "#ab47bc",
                "op_button_hover": "#ba68c8",
                "func_button": "#8e24aa",
                "func_button_hover": "#9c27b0",
                "text_color": "white",
            },
            "green": {
                "name": "Yeşil Tema",
                "bg": "#1b5e20",
                "display_bg": "#1b5e20",
                "display_fg": "#ffffff",
                "num_button": "#2e7d32",
                "num_button_hover": "#388e3c",
                "op_button": "#66bb6a",
                "op_button_hover": "#81c784",
                "func_button": "#43a047",
                "func_button_hover": "#4caf50",
                "text_color": "white",
            }
        }
        
        self.current_theme = "dark"
        self.theme = self.themes[self.current_theme]
        self.theme["button_font"] = ("SF Pro Display", 24)
        self.theme["display_font"] = ("SF Pro Display", 45)
        
        self.setup_gui()
        self.create_menu()
        self.bind_keyboard()

    def setup_gui(self):
        # Ana container
        self.main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=(10, 0))
        
        self.create_display()
        self.create_buttons()
        
        # GitHub kullanıcı adı etiketi
        self.create_github_label()

    def create_display(self):
        # Display container
        display_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        display_frame.pack(fill='x', pady=(40, 20))
        
        self.display = tk.Label(
            display_frame,
            text="0",
            font=self.theme["display_font"],
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            anchor='e',
            padx=20
        )
        self.display.pack(fill='x', expand=True)
        
    def create_button(self, parent, text, row, col, color, colspan=1, rowspan=1):
        button_frame = tk.Frame(
            parent,
            bg=self.theme["bg"]
        )
        button_frame.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,
                         padx=5, pady=5, sticky="nsew")
        
        # Yuvarlak buton efekti için canvas
        canvas = tk.Canvas(
            button_frame,
            width=80 if colspan==1 else 170,
            height=80,
            bg=self.theme["bg"],
            highlightthickness=0
        )
        canvas.pack(expand=True, fill='both')
        
        # Yuvarlak buton çizimi
        button_bg = canvas.create_oval(
            4, 4,
            76 if colspan==1 else 166,
            76,
            fill=color,
            outline=""
        )
        
        # Buton metni
        button_text = canvas.create_text(
            40 if colspan==1 else 85,
            40,
            text=text,
            font=self.theme["button_font"],
            fill=self.theme["text_color"]
        )
        
        # Hover efektleri
        def on_enter(e):
            hover_color = self.get_hover_color(color)
            canvas.itemconfig(button_bg, fill=hover_color)
            
        def on_leave(e):
            canvas.itemconfig(button_bg, fill=color)
            
        def on_click(e):
            self.button_click(text)
            
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        canvas.bind('<Button-1>', on_click)
        
        return button_frame
        
    def create_buttons(self):
        # Önceki buttons_frame varsa temizle
        if self.buttons_frame:
            self.buttons_frame.destroy()
        
        self.buttons_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        self.buttons_frame.pack(expand=True, fill='both')
        
        # Grid yapılandırması
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
            
        # Butonları oluştur
        buttons = [
            ('AC', 0, 0, self.theme["func_button"]),
            ('±', 0, 1, self.theme["func_button"]),
            ('%', 0, 2, self.theme["func_button"]),
            ('÷', 0, 3, self.theme["op_button"]),
            
            ('7', 1, 0, self.theme["num_button"]),
            ('8', 1, 1, self.theme["num_button"]),
            ('9', 1, 2, self.theme["num_button"]),
            ('×', 1, 3, self.theme["op_button"]),
            
            ('4', 2, 0, self.theme["num_button"]),
            ('5', 2, 1, self.theme["num_button"]),
            ('6', 2, 2, self.theme["num_button"]),
            ('−', 2, 3, self.theme["op_button"]),
            
            ('1', 3, 0, self.theme["num_button"]),
            ('2', 3, 1, self.theme["num_button"]),
            ('3', 3, 2, self.theme["num_button"]),
            ('+', 3, 3, self.theme["op_button"]),
        ]
        
        # Normal butonları oluştur
        for (text, row, col, color) in buttons:
            self.create_button(self.buttons_frame, text, row, col, color)
            
        # 0 butonu (geniş)
        self.create_button(self.buttons_frame, '0', 4, 0, self.theme["num_button"], colspan=2)
        # Son sıradaki diğer butonlar
        self.create_button(self.buttons_frame, '.', 4, 2, self.theme["num_button"])
        self.create_button(self.buttons_frame, '=', 4, 3, self.theme["op_button"])
        
    def get_hover_color(self, base_color):
        if base_color == self.theme["num_button"]:
            return self.theme["num_button_hover"]
        elif base_color == self.theme["op_button"]:
            return self.theme["op_button_hover"]
        else:
            return self.theme["func_button_hover"]
            
    def bind_keyboard(self):
        # Klavye kısayolları
        self.root.bind('<Return>', lambda e: self.button_click('='))
        self.root.bind('<Escape>', lambda e: self.button_click('AC'))
        self.root.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        
        # Sayılar
        for i in range(10):
            self.root.bind(str(i), lambda e, digit=i: self.button_click(str(digit)))
            
        # Operatörler
        self.root.bind('+', lambda e: self.button_click('+'))
        self.root.bind('-', lambda e: self.button_click('−'))
        self.root.bind('*', lambda e: self.button_click('×'))
        self.root.bind('/', lambda e: self.button_click('÷'))
        self.root.bind('.', lambda e: self.button_click('.'))
        
    def button_click(self, value):
        current = self.display.cget("text")
        
        if value == 'AC':
            self.display.config(text="0")
            self.current_operation = None
            self.last_number = None
            self.new_number = True
        elif value == '±':
            if current.startswith('-'):
                self.display.config(text=current[1:])
            else:
                self.display.config(text=f"-{current}")
        elif value == '%':
            try:
                result = float(current) / 100
                self.display.config(text=self.format_number(result))
            except:
                self.display.config(text="Hata")
        elif value in ['÷', '×', '−', '+']:
            self.last_number = float(current)
            self.current_operation = value
            self.new_number = True
        elif value == '=':
            if self.current_operation and self.last_number is not None:
                try:
                    current_num = float(current)
                    if self.current_operation == '÷':
                        result = self.last_number / current_num
                    elif self.current_operation == '×':
                        result = self.last_number * current_num
                    elif self.current_operation == '−':
                        result = self.last_number - current_num
                    elif self.current_operation == '+':
                        result = self.last_number + current_num
                        
                    self.display.config(text=self.format_number(result))
                    self.last_number = None
                    self.current_operation = None
                    self.new_number = True
                except:
                    self.display.config(text="Hata")
        else:
            if self.new_number:
                self.display.config(text=value)
                self.new_number = False
            else:
                if current == "0" and value != '.':
                    self.display.config(text=value)
                else:
                    self.display.config(text=current + value)
                    
    def format_number(self, number):
        """Sayıyı güzel formatta göster"""
        if number.is_integer():
            return str(int(number))
        return f"{number:.8f}".rstrip('0').rstrip('.')

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Tema menüsü
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tema", menu=theme_menu)
        
        for theme_id, theme_data in self.themes.items():
            theme_menu.add_command(
                label=theme_data["name"],
                command=lambda t=theme_id: self.change_theme(t)
            )

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.theme = self.themes[theme_name]
        self.theme["button_font"] = ("SF Pro Display", 24)
        self.theme["display_font"] = ("SF Pro Display", 45)
        
        # Ana arka plan rengini güncelle
        self.root.configure(bg=self.theme["bg"])
        self.main_frame.configure(bg=self.theme["bg"])
        
        # Ekranı güncelle
        self.display.configure(
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"]
        )
        
        # Tüm butonları güncelle
        self.recreate_buttons()
        
        # GitHub etiketini de güncelle
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and "Created by" in child.cget("text"):
                        child.configure(
                            bg=self.theme["bg"],
                            fg=self.theme["display_fg"]
                        )

    def recreate_buttons(self):
        # Eski butonları temizle
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        # Butonları yeniden oluştur
        self.create_buttons()

    def create_github_label(self):
        github_frame = tk.Frame(self.root, bg=self.theme["bg"])
        github_frame.pack(fill='x', pady=(0, 5))
        
        github_label = tk.Label(
            github_frame,
            text="Created by @UsainC",
            font=("SF Pro Display", 10),
            bg=self.theme["bg"],
            fg=self.theme["display_fg"],
        )
        github_label.pack(side='right', padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop() 