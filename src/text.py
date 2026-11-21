"""Text cleaning, excerpt and style-feature functions shared by the notebooks."""
import re
import string


def clean_text(text):
    """Remove [bracketed] footnotes/editorial notes and FOOTNOTE headings (same as notebook 02)."""
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"FOOTNOTES?:", " ", text, flags=re.IGNORECASE)
    return text


def chunk(text, n_words=5000, position=0.5):
    """Return n_words consecutive words starting `position` of the way through the book.

    position=0.5 gives the same middle excerpt as notebook 02.
    """
    words = text.split()
    if len(words) <= n_words:
        return " ".join(words)
    start = int((len(words) - n_words) * position)
    return " ".join(words[start:start + n_words])


STYLE_FEATURES = ["avg_sentence_words", "type_token_ratio", "semicolons_per_1000"]


def style_features(text):
    """Three simple writing-style measures of one excerpt (no fitting, so no leakage)."""
    words = text.split()
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    tokens = [w.lower().strip(string.punctuation + "“”‘’—") for w in words]
    tokens = [t for t in tokens if t]
    return {
        "avg_sentence_words": len(words) / max(len(sentences), 1),
        "type_token_ratio": len(set(tokens)) / max(len(tokens), 1),
        "semicolons_per_1000": 1000 * text.count(";") / max(len(words), 1),
    }
