import re
from transformers import T5Tokenizer
import pandas as pd


class T5Preprocessor:
    def __init__(
        self, tokenizer_name="t5-small", max_input_length=64, max_target_length=32
    ):
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name)
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length

    def clean_text(self, text: str) -> str:
        text = str(text).lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def format_row(self, row):
        input_text = f"question: {row['question_clean']} </s>"
        target_text = f"{row['answer_clean']} </s>"
        return pd.Series([input_text, target_text])

    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df["question_clean"] = df["question"].apply(self.clean_text)
        df["answer_clean"] = df["answer"].apply(self.clean_text)
        df[["input_text", "target_text"]] = df.apply(self.format_row, axis=1)
        return df[["input_text", "target_text"]]

    def tokenize_example(self, input_text, target_text):
        input_enc = self.tokenizer.encode_plus(
            input_text,
            max_length=self.max_input_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        target_enc = self.tokenizer.encode_plus(
            target_text,
            max_length=self.max_target_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return input_enc, target_enc
