import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pytube import YouTube

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube MP3 Downloader")

        style = ttk.Style()
        style.theme_use('clam')

        self.label = tk.Label(master, text="Insira o link do YouTube:", font=("Arial", 12))
        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.entry = tk.Entry(master, width=50, font=("Arial", 12))
        self.entry.grid(row=1, column=0, padx=10, pady=5)

        self.clear_button = ttk.Button(master, text="Limpar", command=self.clear_entry, style='Rounded.TButton')
        self.clear_button.grid(row=1, column=1, padx=5, pady=5)

        self.validate_button = ttk.Button(master, text="Validar Qualidade", command=self.validate_quality, style='Rounded.TButton')
        self.validate_button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.quality_label = tk.Label(master, text="Escolha a qualidade da música:", font=("Arial", 12))
        self.quality_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.quality_var = tk.StringVar(master)
        self.quality_options = ["Escolha uma opção..."]
        self.quality_menu = tk.OptionMenu(master, self.quality_var, *self.quality_options)
        self.quality_menu.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.folder_label = tk.Label(master, text="Pasta selecionada:", font=("Arial", 12))
        self.folder_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        self.selected_folder = tk.StringVar()
        self.selected_folder.set("Nenhuma pasta selecionada")
        self.folder_display = tk.Label(master, textvariable=self.selected_folder, font=("Arial", 12))
        self.folder_display.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.folder_button = ttk.Button(master, text="Escolher Pasta", command=self.choose_folder, style='Rounded.TButton')
        self.folder_button.grid(row=6, column=2, padx=5, pady=5)

        self.download_button = ttk.Button(master, text="Baixar", command=self.download, style='Rounded.TButton')
        self.download_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

        self.progress_label = tk.Label(master, text="", font=("Arial", 12))
        self.progress_label.grid(row=8, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        self.round_buttons()

    def round_buttons(self):
        style = ttk.Style()
        style.configure('Rounded.TButton', borderwidth=0, bordercolor='white', focusthickness=3, focuscolor='none', background='#0078d7', foreground='white', relief=tk.FLAT, font=('Arial', 12))
        style.map('Rounded.TButton', background=[('active', '#005FAB')])

    def clear_entry(self):
        self.entry.delete(0, tk.END)
        self.progress_label.config(text="")

    def choose_folder(self):
        self.download_folder = filedialog.askdirectory()
        self.selected_folder.set(self.download_folder)

    def get_available_qualities(self, link):
        try:
            yt = YouTube(link)
            streams = yt.streams.filter(only_audio=True)
            available_qualities = [stream.abr for stream in streams if stream.abr.endswith("kbps")]
            available_qualities.sort(key=lambda x: int(x[:-4]))
            return available_qualities
        except Exception as e:
            print("Erro ao obter as qualidades disponíveis:", e)
            return []

    def validate_quality(self):
        link = self.entry.get()

        if not link:
            messagebox.showerror("Erro", "Insira um link do YouTube!")
            return

        qualities = self.get_available_qualities(link)
        if qualities:
            self.quality_options = ["Escolha uma opção..."] + qualities
            self.quality_var.set(self.quality_options[0])
            self.quality_menu['menu'].delete(0, 'end')
            for quality in self.quality_options:
                self.quality_menu['menu'].add_command(label=quality, command=tk._setit(self.quality_var, quality))
        else:
            messagebox.showerror("Erro", "Não há qualidades disponíveis para este vídeo.")

    def download(self):
        link = self.entry.get()
        quality = self.quality_var.get()

        if not link:
            messagebox.showerror("Erro", "Insira um link do YouTube!")
            return

        if quality == "Escolha uma opção...":
            messagebox.showerror("Erro", "Selecione uma qualidade para baixar.")
            return

        if not os.path.isdir(self.download_folder):
            messagebox.showerror("Erro", "Selecione uma pasta de destino válida.")
            return

        try:
            yt = YouTube(link)
            stream = yt.streams.filter(only_audio=True, abr=quality).first()

            if stream:
                self.download_button.config(state="disabled")
                self.progress_label.config(text="Download em andamento...")
                self.master.update_idletasks()

                title = yt.title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

                stream.download(output_path=self.download_folder, filename=f"{title}.mp3")
                self.progress_label.config(text="Download completo!")
            else:
                messagebox.showerror("Erro", "A qualidade selecionada não está disponível para este vídeo.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante o download: {e}")
        finally:
            self.download_button.config(state="normal")

root = tk.Tk()
app = YouTubeDownloaderApp(root)
root.mainloop()
