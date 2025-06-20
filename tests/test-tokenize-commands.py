from ai_commander.tokenizer import Wb95Tokenizer

# Load tokenizer
tokenizer = Wb95Tokenizer("tests/generated/test_tokenizer_vocab.json")

# Load example commands
# with open("examples/example_commands.txt", "r", encoding="utf-8") as f:
#     commands = [line.strip() for line in f.readlines() if line.strip()]

# Process each command
# for i, command in enumerate(commands):
command = '<1_1_17/2/2/2><2371><MOVE><1_1_17/2/2/1><2372>'
print(f"\n--- Example {1} ---")
print(f"Original command: {command}")

tokens = tokenizer.tokenize(command)
ids = tokenizer.convert_tokens_to_ids(tokens)
decoded = tokenizer.decode(ids)
print(f"Tokens: {tokens}")
print(f"Input IDs: {ids}")
print(f"Decoded: {decoded}")