import threading
import tkinter as tk
from tkinter import filedialog
import os
import webview
from pytube import YouTube
from flask import Flask


app = Flask(__name__, static_url_path='/static')

class YouTubeDownloaderApp:
    MAIN_AUDIO_QUALITIES = ["256kbps", "192kbps", "128kbps"]

    def __init__(self):
        self.quality_cache = {}

    def validate_quality(self, link):
        if link in self.quality_cache:
            self.update_quality_options(self.quality_cache[link])
            return

        def analyze_qualities(callback):
            try:
                yt = YouTube(link)
                streams = yt.streams.filter(only_audio=True)
                available_qualities = [stream.abr for stream in streams if stream.abr.endswith("kbps")]
                if available_qualities:
                    available_qualities.sort(key=lambda x: int(x[:-4]))
                    self.quality_cache[link] = available_qualities
                    callback(available_qualities)
                else:
                    self.show_alert("Nenhuma qualidade de áudio disponível para este vídeo.")
                    callback([])
            except Exception as e:
                print("Erro ao obter as qualidades disponíveis:", e)
                self.show_alert("Erro ao obter as qualidades disponíveis.")
                callback([])

        def callback_wrapper(qualities):
            # Use o nome do arquivo Python atual (__file__) para obter o diretório estático
            static_dir = os.path.dirname(os.path.abspath(__file__))
            webview.windows[0].evaluate_js(f"updateQualityOptions({qualities})", static_dir)

        thread = threading.Thread(target=analyze_qualities, args=(callback_wrapper,))
        thread.start()

    def update_quality_options(self, qualities):
        # Use o nome do arquivo Python atual (__file__) para obter o diretório estático
        static_dir = os.path.dirname(os.path.abspath(__file__))
        webview.windows[0].evaluate_js(f"updateQualityOptions({qualities})", static_dir)

    def choose_folder(self):
        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal
        download_folder = filedialog.askdirectory()

        if download_folder:
            mp3_files = [file for file in os.listdir(download_folder) if file.endswith(".mp3")]
            mp3_files_string = "\n".join(mp3_files)
            self.show_alert(f"Arquivos .mp3 encontrados na pasta selecionada:\n{mp3_files_string}")

        root.destroy()  # Destroi a janela após a seleção
        return download_folder

    def download(self, link, quality, download_folder):
        try:
            yt = YouTube(link)
            stream = yt.streams.filter(only_audio=True, abr=quality).first()

            if stream:
                title = yt.title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
                update_progress("Fazendo download, aguarde...")
                stream.download(output_path=download_folder, filename=f"{title}.mp3")
            else:
                self.show_alert("A qualidade selecionada não está disponível para este vídeo.")
        except Exception as e:
            self.show_alert(f"Erro durante o download: {e}")

    def show_alert(self, message):
        print(message)  # Mostra a mensagem no terminal

def update_progress(message):
    print(message)  # Mostra a mensagem no terminal

if __name__ == '__main__':
    api = YouTubeDownloaderApp()
    webview.create_window('YouTube MP3 Downloader', './static/index.html', js_api=api)
    webview.start(debug=False)
