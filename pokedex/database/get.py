# -*- encoding: utf-8 -*-

import os
import requests
import zlib
from progressbar import ProgressBar

from .. import var_resource_path


def download_database():
    target = os.path.join(var_resource_path, "veekun-pokedex.sqlite")
    url = "http://veekun.com/static/pokedex/downloads/veekun-pokedex.sqlite.gz"
    
    if os.path.isfile(target):
        return

    request = requests.get(url, stream=True)
    total_length = int(request.headers.get("content-length"))
    bytes_done = 0
    gzipped = ""

    print("Downloading Veekun Pokédex database...")
    with ProgressBar(max_value=total_length) as bar:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                gzipped += chunk
                bytes_done += len(chunk)
                bar.update(bytes_done)

    decompressed_data = zlib.decompress(gzipped, 16+zlib.MAX_WBITS)

    with open(target, "wb") as file:
        file.write(decompressed_data)
