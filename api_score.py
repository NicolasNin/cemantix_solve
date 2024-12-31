import io
import json
import requests
from abc import ABC, abstractmethod

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': '*/*',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
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
    if response.status_code == 200:
        try:
            # Debug the raw content
            print("Raw content bytes:", [x for x in response.content[:20]])  # First 20 bytes
            print("Content length:", len(response.content))
            print("response headers",response.headers)
            # Try different decodings
            try:
                # Try UTF-8 with ignore
                decoded = response.content.decode('utf-8', errors='ignore')
                print("UTF-8 decoded:", decoded)
                return json.loads(decoded)
            except:
                # Try removing BOM or other prefixes
                content = response.content
                if content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
                    content = content[3:]
                elif content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'):  # UTF-16 BOM
                    content = content[2:]
                
                print("After BOM removal:", content[:20])
                return json.loads(content.decode('utf-8', errors='ignore'))
                
        except Exception as e:
            print(f"Error type: {type(e)}")
            print(f"Error decoding response: {e}")
            return "error"
    return "error"
    
class ScoreStrategy(ABC):
    @abstractmethod
    def get_score(self, word: str):
        pass

# Concrete implementation for external API
class ExternalAPIStrategy(ScoreStrategy):
    def __init__(self, api_url=None):  # You might need other params
        self.api_url = api_url
    
    def get_score(self, word: str):
        # Your existing external API call implementation
        return get_score(word)

# Concrete implementation for local game
class LocalGameStrategy(ScoreStrategy):
    def __init__(self, game):
        self.game = game
    
    def get_score(self, word: str):
        return self.game.get_score(word)