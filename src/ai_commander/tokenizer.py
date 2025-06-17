import json
import re

class Wb95Tokenizer:
    def __init__(self, vocab_path: str = None):
        if vocab_path:
            with open(vocab_path, "r", encoding="utf-8") as f:
                self.vocab = json.load(f)
            self.id2token = {v: k for k, v in self.vocab.items()}
        else:
            self.vocab = {}
            self.id2token = {}
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"

    def tokenize(self, command: str) -> list:
        tokens = []

        parts = re.findall(r"<(.*?)>", command)
        for i, part in enumerate(parts):
            if "/" in part and "_" in part:
                company, battalion, regiment = part.split("/")[0].split("_")
                strength, manuever, movement = part.split("/")[1:]
                tokens.extend([
                    f"COM_{company}",
                    f"BAT_{battalion}",
                    f"REG_{regiment}",
                    f"STR_{strength}",
                    f"MAN_{manuever}",
                    f"MOV_{movement}"
                ])
            elif part.isdigit():
                if i == 1:
                    tokens.append(f"HEX_START_{part}")
                elif i == 4:
                    tokens.append(f"HEX_END_{part}")
                else:
                    tokens.append(f"HEX_{part}")
            elif part.isalpha():
                tokens.append(f"ACTION_{part.upper()}")
            else:
                tokens.append(part)

        return tokens

    def convert_tokens_to_ids(self, tokens: list) -> list:
        return [self.vocab.get(token, self.vocab[self.unk_token]) for token in tokens]

    def __call__(self, command: str) -> dict:
        tokens = self.tokenize(command)
        input_ids = self.convert_tokens_to_ids(tokens)
        return {
            "input_ids": input_ids,
            "attention_mask": [1] * len(input_ids)
        }

    def decode(self, ids: list) -> str:
        return " ".join(self.id2token.get(i, self.unk_token) for i in ids)

    def save_vocab(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=4)

    @classmethod
    def from_pretrained(cls, path: str):
        return cls(path)