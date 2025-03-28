import os
from yt_dlp import YoutubeDL
from tqdm import tqdm

# Variáveis globais para controlar a barra de progresso
pbar = None

def create_directory(directory_name):
    """
    Cria uma pasta com o nome especificado, caso ela não exista.
    """
    directory_name = f"../{directory_name}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def progress_hook(d):
    global pbar

    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)

        # Inicia a barra de progresso quando o total de bytes é conhecido
        if pbar is None and total_bytes > 0:
            pbar = tqdm(total=total_bytes, unit='B', unit_scale=True)

        # Atualiza a barra de progresso com os bytes baixados
        if pbar:
            pbar.n = downloaded_bytes
            pbar.refresh()

    elif d['status'] == 'finished':
        if pbar:
            pbar.close()
            print("\nDownload concluído!")

def download_youtube_video(url, only_audio):
    # Cria pastas para salvar os arquivos
    create_directory("music")
    create_directory("movies")

    # Define o caminho de saída com base na escolha
    output_directory = "../music/%(title)s.%(ext)s" if only_audio else "../movies/%(title)s.%(ext)s"

    # Define as opções com base na escolha do usuário
    if only_audio:
        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [progress_hook],
            'outtmpl': output_directory,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Qualidade ajustada para 128kbps
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]/best',
            'progress_hooks': [progress_hook],
            'outtmpl': output_directory,
            'merge_output_format': 'mp4',
        }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():

    # Exemplo de uso
    url = input("Insira a URL do vídeo do YouTube: ")
    choice = input("Deseja baixar apenas o áudio (S/N)? ").strip().lower()

    # Determina a escolha do usuário
    only_audio = choice == 's'

    download_youtube_video(url, only_audio)

if __name__ == "__main__":
    main()
