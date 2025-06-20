import os
import json
from ai_commander.tokenizer import Wb95Tokenizer

INPUT_PATH = "tests/sources/example_wb95_commands.txt"
OUTPUT_PATH = "tests/generated/test_tokenizer_vocab.json"

def build_vocab_from_examples(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        commands = [line.strip() for line in f.readlines() if line.strip()]

    token_set = set()

    tokenizer = Wb95Tokenizer(vocab_path=None)

    for cmd in commands:
        tokens = tokenizer.tokenize(cmd)
        token_set.update(tokens)

    token_list = sorted(token_set)

    vocab = {
        "<PAD>": 0,
        "<UNK>": 1,
    }

    for i, token in enumerate(token_list, start=2):
        vocab[token] = i

    return vocab

if __name__ == "__main__":
    print(f"🔍 Building vocab from {INPUT_PATH}...")

    vocab = build_vocab_from_examples(INPUT_PATH)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=4)

    print(f"✅ Vocab saved to {OUTPUT_PATH} with {len(vocab)} entries.")