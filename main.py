import os
import time

from yt_dlp import YoutubeDL
from tqdm import tqdm

from config import config

pbar = None

def create_directory(directory_name):
    if not os.path.exists("../storage") and not os.path.exists(f"../{directory_name}"):
      os.makedirs(directory_name)

def progress_hook(d):
    global pbar

    if d["status"] == "downloading":

        # DOWNLOAD FRAGMENTADO
        if d.get("fragment_count"):
            current = d.get("fragment_index", 0) + 1
            total = d["fragment_count"]
            print(f"\rFragmento {current}/{total}", end="", flush=True)

        # DOWNLOAD POR BYTES
        else:
            total_bytes = d.get("total_bytes", 0)
            downloaded_bytes = d.get("downloaded_bytes", 0)

            if pbar is None and total_bytes > 0:
                pbar = tqdm(total=total_bytes, unit="B", unit_scale=True)

            if pbar:
                pbar.n = downloaded_bytes
                pbar.refresh()

    elif d["status"] == "finished":
        if pbar:
            pbar.close()
            pbar = None
        print("\nDownload concluído!")

def download_with_timeout(url, only_audio):
    create_directory("music")
    create_directory("movies")

    output_directory = None
    if os.path.exists("../storage"):
      output_directory = (
        "../storage/music/%(title)s.%(ext)s"
        if only_audio else
        "../storage/movies/%(title)s.%(ext)s"
      )
    else:
       output_directory = (
        "../music/%(title)s.%(ext)s"
        if only_audio else
        "../movies/%(title)s.%(ext)s"
      )

    ydl_opts = {
        "format": "bestaudio/best" if only_audio else "bestvideo[height<=360]+bestaudio/best",
        "outtmpl": output_directory,
        "progress_hooks": [progress_hook],
        "continuedl": True,
        "ignoreerrors": False,
        "abort_on_error": False,
        "socket_timeout": config.SOCKET_TIMEOUT,
        "retries": 1,
        "fragment_retries": 1,
    }

    if only_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 'best',  # Qualidade ajustada para 128kbps
         }]

    offline_time = 0

    while offline_time < config.MAX_OFFLINE_TIME:
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return  # sucesso


        except Exception as e:

            if pbar:
                pbar.close()

            msg = str(e)

            if "Errno 7" in msg or "timed out" in msg:
              offline_time += config.RETRY_INTERVAL
              print(
                f"\nErro!!  ({offline_time}s/{config.MAX_OFFLINE_TIME}s).\n",
                f"_"*30,
                f"\n{type(e).__name__}: {e} \n",
                f"_"*30,
                f"\n\nTentando novamente em {config.RETRY_INTERVAL}s..."
              )
              time.sleep(config.RETRY_INTERVAL)
            elif "video unable" in msg.lower():
              raise
              main()
            else:
              raise

    raise SystemExit("Internet indisponível por tempo excessivo. Encerrando.")

def main():
    url = input("Insira a URL do vídeo do YouTube: ")
    choice = input("Deseja baixar apenas o áudio (S/N)? ").strip().lower()

    only_audio = choice == "s"
    download_with_timeout(url, only_audio)

if __name__ == "__main__":
    main()
