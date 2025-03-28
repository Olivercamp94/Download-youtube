# Pytube Video Downloader

Este projeto consiste em um script Python para baixar vídeos do YouTube utilizando a biblioteca `pytube`. Ele permite baixar vídeos na melhor qualidade disponível a partir de uma lista de URLs fornecidas.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/seu-repo.git
    ```

2. Instale as dependências com pip:

    ```bash
    pip install pytube
    ```

## Uso

1. Substitua as URLs na lista `urls` pelo link dos vídeos do YouTube que você deseja baixar.

2. Execute o script Python:

    ```bash
    python video_downloader.py
    ```

## Exemplo

```python
from pytube import YouTube
from tqdm import tqdm

# URL do vídeo do YouTube
urls = [
    'https://www.youtube.com/watch?v=GNsuF4xB80E&list=PL0Zuz27SZ-6NamGNr7dEqzNFEcZ_FAUVX&index=7'
]

for url in urls:
    # Criar um objeto YouTube
    yt = YouTube(url)
    # Baixar o vídeo na melhor qualidade disponível
    video = yt.streams.get_highest_resolution()

    # Iniciar o download
    print(f'Baixando: {video.title}')
    with tqdm(total=video.filesize, unit='B', unit_scale=True, desc=video.title, ascii=True) as progress_bar:
        video.download(output_path='.', filename=video.title, filename_prefix='')
        progress_bar.update(video.filesize)

    print("Download concluído!")
# Download-youtube
# Download-youtube
# Download-youtube
# Download-youtube
