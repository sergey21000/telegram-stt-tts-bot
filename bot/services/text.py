import re


class TextPipeline:
    opening_thinking_tags = ['<think>', '&lt;think&gt;']
    closing_thinking_tags = ['</think>', '&lt;/think&gt;']
    all_thinking_tags = [*opening_thinking_tags, *closing_thinking_tags]


    @classmethod
    def clean_thinking_tags(cls, text: str) -> str:
        for open_tag, close_tag in zip(cls.opening_thinking_tags, cls.closing_thinking_tags):
            pattern = rf'{open_tag}.*?{close_tag}'
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        return text


    @staticmethod
    def transliterate_english_to_russian(text: str) -> str:
        translit_map = {
            'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е',
            'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'ж',
            'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
            'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т',
            'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'й',
            'z': 'з',
            'A': 'А', 'B': 'Б', 'C': 'К', 'D': 'Д', 'E': 'Е',
            'F': 'Ф', 'G': 'Г', 'H': 'Х', 'I': 'И', 'J': 'Ж',
            'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О',
            'P': 'П', 'Q': 'К', 'R': 'Р', 'S': 'С', 'T': 'Т',
            'U': 'У', 'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Й',
            'Z': 'З',
            '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
            '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять',
            '+': ' плюс ', '-': ' минус ', '=': ' равно ',
            '*': ' умножить ', '/': ' разделить ', '%': ' процент ',
        }
        
        def transliterate_char(char):
            return translit_map.get(char, char)
        
        return ''.join(transliterate_char(c) for c in text)


    @classmethod
    def clean_text_before_edge_tts(cls, text: str) -> str:
        text = re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9\s.,!?;:()\"'-]", '', text)
        text = re.sub(r'[\"\'«»]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @classmethod
    def clean_text_before_vosk_tts(cls, text: str) -> str:
        text = cls.transliterate_english_to_russian(text)
        text = re.sub(r"[^a-zA-Zа-яА-Я0-9\s.,!?;:()\"'-]", '', text)
        text = re.sub(r'[\"\'«»]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
