import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import subprocess
import os
import sys
from PIL import Image, ImageTk, ImageDraw
import platform

class RoundButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg, fg, text, command=None):
        super().__init__(parent, width=width, height=height,
                         bg=bg, highlightthickness=0)
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.bg = bg
        self.fg = fg
        self.text = text
        self.command = command

        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self._draw()

    def _draw(self):
        self.delete("all")
        self._round_rectangle(0, 0, self.width, self.height, self.corner_radius, fill=self.bg)
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                         fill=self.fg, font=("Arial", 12))

    def _round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_press(self, event):
        self._draw()
        self._round_rectangle(0, 0, self.width, self.height, self.corner_radius, fill="#AAAAAA")

    def _on_release(self, event):
        self._draw()
        if self.command:
            self.command()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Проверка на Читы")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"600x400")
        self.configure(bg="#333333")

        try:
            script_dir = self.get_script_directory()
            icon_path = os.path.join(script_dir, "icon.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Не удалось установить иконку: {e}")

        self.bg_color = "#333333"
        self.fg_color = "#ffffff"
        self.button_bg = "#555555"
        self.button_fg = "#ffffff"
        self.highlight_color = "#777777"

        self.title_font = ("Arial", 16, "bold")
        self.normal_font = ("Arial", 12)

        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.info_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.programs_button = RoundButton(
            self.button_frame,
            width=170,
            height=40,
            corner_radius=10,
            bg=self.button_bg,
            fg=self.fg_color,
            text="Открыть Программы",
            command=self.show_programs_window
        )
        self.programs_button.pack(pady=10, fill=tk.X)


        info_text = "Эта программа предназначена для выявления читов.\n" \
                    "Создатель: Модератор not_cheater"

        self.info_text = tk.Text(
            self.info_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            wrap=tk.WORD,
            borderwidth=0,
            relief=tk.FLAT,
            font=self.normal_font
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state=tk.DISABLED)

        self.button_frame.configure(bg=self.bg_color)
        self.info_frame.configure(bg=self.bg_color)

        self.avatar_label = None

        try:
            script_dir = self.get_script_directory()
            avatar_path = os.path.join(script_dir, "avatar.png")
            self.avatar_image = Image.open(avatar_path)

            resized_image = self.avatar_image.resize((100, 100),
                                                     Image.LANCZOS)
            self.avatar_photo = ImageTk.PhotoImage(resized_image)
            self.avatar_label = tk.Label(self.main_frame, image=self.avatar_photo, bg=self.bg_color)

            self.avatar_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

            self.avatar_label.image = self.avatar_photo

        except FileNotFoundError:
            print("Аватар не найден (avatar.png)")
        except Exception as e:
            print(f"Ошибка при загрузке аватара: {e}")

    def show_programs_window(self):
        programs_window = tk.Toplevel(self)
        programs_window.title("Открыть Программы")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 0.2)
        window_height = int(screen_height * 0.3)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        programs_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        programs_window.configure(bg=self.bg_color)

        script_directory = self.get_script_directory()

        programs = {
            "USBDeview": ("USBDeview.exe", None),
            "Everything": ("Everything.exe", "vilonity|avalon|kitekat|paste.cc|skyline.fix|masonlite|amphetamine|simplicity|apfetamine|trinity|clarity|NovazBesting|vlone|invis.hack|AMTH|skidware|infinity|AdolfRust|ComputeStringHash|dummy_ptr|facepunch.graphics|norecoil|ExternalCheat_NoRecoil|GxOne|RustExploit_Injector|KaboomCheat|UnderHack|Facepunch.Sharp|BasicLand|GOPOTA|invis|money_rain|superiority|infinity.|astrahookie|geroin|dolbaebfree|novazbesting|CatChair|0xcheat|Dootpeaker.space|skyline.one|lghub|brend|extreme|UnityCrashHandler64|imgui|halal.exe|reg.exe|ak47|berda|Deluxe|Nova|keyran|com.swiftsoft|ANW|UG.dll|cartine.html|plague.dll|plaguecrack.dll|plaguepast.dll|suckmaster|spermaHookie|winhttp.dll|skidware.cc|laze.dll|mortemsuck|AnywareFree|MyCheat.dll|Dast"),
            "LastActivityView": ("LastActivityView.exe", None),
            "ShellBags Analizer": ("ShellBag_analizer.exe", None)
        }

        button_container = tk.Frame(programs_window, bg=self.bg_color)
        button_container.pack(expand=True, fill="both")
        button_width = 150
        button_height = 40
        for name, (filename, copyable_text) in programs.items():
            full_path = os.path.join(script_directory, filename)

            program_button = RoundButton(
                button_container,
                width=button_width,
                height=button_height,
                corner_radius=10,
                bg=self.button_bg,
                fg=self.fg_color,
                text=name,
                command=lambda p=full_path, n=name: self.attempt_run_program(p, n, programs_window)

            )
            program_button.pack(pady=5, padx=10)

            if copyable_text:
                text_widget = tk.Text(button_container, height=2, width=30, bg=self.bg_color, fg=self.fg_color,
                                      wrap=tk.WORD, font=self.normal_font)
                text_widget.insert(tk.END, copyable_text)
                text_widget.config(state=tk.DISABLED)
                text_widget.pack(pady=2)

        try:
            script_dir = self.get_script_directory()
            icon_path = os.path.join(script_dir, "icon.ico")
            programs_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Не удалось установить иконку: {e}")

        programs_window.protocol("WM_DELETE_WINDOW", self.destroy)

    def attempt_run_program(self, path, program_name, programs_window):
        try:
            self.run_program(path)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Программа {program_name} не найдена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при запуске {program_name}: {e}")

    def run_program(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")

        try:
            subprocess.Popen([path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                             shell=True)
        except OSError as e:
            if e.winerror == 5:
                messagebox.showerror("Ошибка", "Недостаточно прав для запуска этой программы от имени администратора.")
            else:
                messagebox.showerror("Ошибка", f"Произошла ошибка при запуске {path}: {e}")

    def get_script_directory(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def destroy(self):
        if self.avatar_photo:
            self.avatar_photo = None
        super().destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()