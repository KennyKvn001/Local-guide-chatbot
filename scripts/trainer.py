from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
)
from datasets import Dataset
import pandas as pd
import torch
import matplotlib.pyplot as plt

class T5Trainer:
    def __init__(
        self,
        model_name= "t5-small",
        max_input_length= 64,
        max_target_length=32,
    ):
        self.model_name = model_name
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length
        self.trainer = None

    def load_dataset(self, csv_path: str):
        df = pd.read_csv(csv_path)[["input_text", "target_text"]].dropna()
        return Dataset.from_pandas(df)

    def preprocess(self, examples):
        model_inputs = self.tokenizer(
            examples["input_text"],
            max_length=self.max_input_length,
            padding="max_length",
            truncation=True,
        )
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(
                examples["target_text"],
                max_length=self.max_target_length,
                padding="max_length",
                truncation=True,
            )
        labels["input_ids"] = [
            [(token if token != self.tokenizer.pad_token_id else -100) for token in label]
            for label in labels["input_ids"]
        ]
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def prepare_data(self, dataset, val_ratio: float = 0.15):
        train_test = dataset.train_test_split(test_size=val_ratio, seed=42)
        tokenized_train = train_test["train"].map(self.preprocess, batched=True)
        tokenized_val = train_test["test"].map(self.preprocess, batched=True)
        return tokenized_train, tokenized_val

    def _plot_losses(self, log_history):
        """Internal method to plot training/validation losses"""
        train_losses = [log['loss'] for log in log_history if 'loss' in log]
        val_losses = [log['eval_loss'] for log in log_history if 'eval_loss' in log]
        
        plt.figure(figsize=(10, 5))
        plt.plot(train_losses, label="Training Loss", marker='o')
        plt.plot(val_losses, label="Validation Loss", marker='o')
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training vs Validation Loss")
        plt.legend()
        plt.grid()
        plt.show()

    def train(
        self,
        train_dataset,
        val_dataset,
        output_dir= "t5_rwanda_model",
        epochs= 4,
        batch_size= 8,
        lr= 5e-5,
    ):
        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            evaluation_strategy="epoch",
            logging_strategy="epoch",
            save_strategy="epoch",
            num_train_epochs=epochs,
            learning_rate=lr,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            fp16=torch.cuda.is_available(),
        )

        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=self.tokenizer,
            data_collator=DataCollatorForSeq2Seq(
                tokenizer=self.tokenizer,
                model=self.model,
                label_pad_token_id=-100,
            ),
        )

        # Train and plot losses automatically
        print("Training started...")
        self.trainer.train()
        print("Training completed!")
        
        # Plot losses from the trainer's log history
        self._plot_losses(self.trainer.state.log_history)
        
        # Save model
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        print(f"Model saved to {output_dir}")

        return self.trainer  # Return the Hugging Face Trainer for further analysis


# Usage Example
if __name__ == "__main__":
    # Initialize and train
    trainer = T5Trainer()
    raw_ds = trainer.load_dataset("processed_t5_rwanda_data.csv")
    train_ds, val_ds = trainer.prepare_data(raw_ds, val_ratio=0.15)
    
    # Train with automatic plotting
    hf_trainer = trainer.train(
        train_ds, 
        val_ds, 
        output_dir="t5_rwanda_finetuned", 
        epochs=4
    )
    