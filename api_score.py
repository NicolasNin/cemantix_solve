import zstandard as zstd
import io
import json
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': '*/*',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://cemantix.certitudes.org/',
    'Origin': 'https://cemantix.certitudes.org',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive'
}

def get_score(word):
    url = 'https://cemantix.certitudes.org/score'
    data = {
        'word': word
    }
    response = requests.post(url, headers=headers, data=data)

    # Print response
    print(response.status_code)
    if response.status_code == 200:
        dctx = zstd.ZstdDecompressor()
        with io.BytesIO(response.content) as compressed:
            with dctx.stream_reader(compressed) as reader:
                # Read all decompressed data
                decompressed_data = reader.read()
        result = json.loads(decompressed_data)
        return result
    else:
        print("error",response.status_code)
        return "error"