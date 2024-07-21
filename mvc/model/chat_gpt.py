import requests

from Acess.secret import GPTKEY


class ChatGPT:

    def __init__(self):
        self.url = 'https://api.openai.com/v1/chat/completions'
        self.key = GPTKEY
        self.header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.key}'
        }
        self.message = ""
        self.body = {}

    def set_message(self):
        self.message = '{}'

    def set_body(self, content: str):
        self.body = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f'{content}'}],
            "temperature": 0.7
        }

    def send_prompt(self, prompt: str) -> str:
        self.set_message()
        self.set_body(self.message.format(prompt))
        return requests.post(self.url, headers=self.header, json=self.body).json()\
            .get('choices')[0]\
            .get('message')\
            .get('content')

    def generate_song_list(self, description: str, num_songs: int) -> str:
        prompt = f'Please generate me a playlist of {num_songs} that fits this description: ' \
                 f'{description}.' \
                 f'Please respond with ONLY the song names and artist in the format' \
                 f'"song" - "artist". Please do not give me a numbered list'
        return self.send_prompt(prompt)

