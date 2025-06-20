import random

ADJECTIVES = [
    "agile", "brave", "clever", "daring", "eager", "fierce", "gentle",
    "happy", "jolly", "keen", "lively", "mighty", "nifty", "proud",
    "quirky", "rapid", "shy", "tidy", "upbeat", "vivid", "witty", "zany"
]

NAMES = [
    "turing", "curie", "newton", "tesla", "einstein", "lovelace",
    "bohr", "kepler", "galileo", "hawking", "fermi", "darwin",
    "ohm", "boyle", "morse", "feynman", "aisha"
]

def generate_readable_name():
    return f"{random.choice(ADJECTIVES)}_{random.choice(NAMES)}"