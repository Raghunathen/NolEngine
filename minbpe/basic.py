import unicodedata
from collections import Counter
from tqdm.notebook import trange
# Helper functions
def get_stats(ids):
    """
    Returns counts of consecutive pairs in the list of token ids.
    """
    return Counter(zip(ids, ids[1:]))

def merge(ids, pair, new_token_id):
    """
    Replace occurrences of a pair in ids with a new token id.
    """
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
            new_ids.append(new_token_id)
            i += 2  # Skip the pair
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids

def render_token(t: bytes) -> str:
    """
    Render a token (in bytes) to a string, escaping control characters.
    """
    return t.decode('utf-8', errors='replace')


# BPE Tokenizer class
class BPETokenizer:
    def __init__(self):
        self.vocab = {}           # Mapping from token id to token string
        self.merges = {}          # Mapping of (pair) -> new token id
        self.special_tokens = {}  # Special tokens like <endoftext>
        self.pattern = ""         # Optional: Can be used for pattern-based tokenization

    def train(self, text, vocab_size):
        """
        Train the BPE tokenizer on the given text, up to the desired vocab_size.
        """
        text_bytes = text.encode("utf-8")
        ids = list(text_bytes)

        # Initialize vocab with individual byte-level tokens
        self.vocab = {i: bytes([i]) for i in range(256)}
        num_merges = vocab_size - len(self.vocab)

        for i in trange(num_merges):
            stats = get_stats(ids)
            if not stats:
                break

            pair = max(stats, key=stats.get)
            new_token_id = 256 + i

            ids = merge(ids, pair, new_token_id)
            self.merges[pair] = new_token_id
            self.vocab[new_token_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

    def encode(self, text):
        """
        Encode text into a list of token ids.
        """
        text_bytes = text.encode("utf-8")
        ids = list(text_bytes)

        for pair, new_id in self.merges.items():
            ids = merge(ids, pair, new_id)

        return ids

    def decode(self, ids):
        """
        Decode a list of token ids back into a string.
        """
        tokens = [self.vocab[idx] for idx in ids]
        return b"".join(tokens).decode("utf-8", errors="replace")

    def save(self, file_prefix):
        """
        Save the tokenizer model (merges, vocab) to files.
        """
        model_file = file_prefix + ".model"
        with open(model_file, "w") as f:
            f.write("bpe v1\n")
            f.write(f"{self.pattern}\n")
            f.write(f"{len(self.special_tokens)}\n")
            for special, idx in self.special_tokens.items():
                f.write(f"{special} {idx}\n")
            for (idx1, idx2), new_token_id in self.merges.items():
                f.write(f"{idx1} {idx2}\n")

        vocab_file = file_prefix + ".vocab"
        with open(vocab_file, "w", encoding="utf-8") as f:
            for idx, token in self.vocab.items():
                f.write(f"{render_token(token)} {idx}\n")

    def load(self, model_file):
        """
        Load the tokenizer model from a file.
        """
        assert model_file.endswith(".model")
        self.merges = {}
        self.special_tokens = {}
        idx = 256

        with open(model_file, 'r', encoding="utf-8") as f:
            version = f.readline().strip()
            assert version == "bpe v1"

            self.pattern = f.readline().strip()
            num_special = int(f.readline().strip())

            for _ in range(num_special):
                line = f.readline().strip()
                try:
                    special, special_idx = line.split()
                    self.special_tokens[special] = int(special_idx)
                except ValueError:
                    print(f"Error reading special token line: '{line}'")
                    continue

            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    try:
                        idx1, idx2 = map(int, parts)
                        self.merges[(idx1, idx2)] = idx
                        idx += 1
                    except ValueError:
                        print(f"Error parsing merge line: '{line}'")

        self.vocab = self._build_vocab()

    def _build_vocab(self):
        """
        Rebuild vocab from the merges.
        """
        vocab = {i: bytes([i]) for i in range(256)}
        for (p0, p1), new_id in self.merges.items():
            vocab[new_id] = vocab[p0] + vocab[p1]
        for special, idx in self.special_tokens.items():
            vocab[idx] = special.encode("utf-8")
        return vocab
