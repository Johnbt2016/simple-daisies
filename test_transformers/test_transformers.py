from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import sentencepiece

tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

def generate_summary(text, min_length = 80, max_length=150):
    """
    Generate a summarized version of given text.
    
    Parameters
    ----------
    min_length: int
        The minimum word count of the summary
    max_length: int
        The maximum word count of the summary  

    Returns
    -------
    str
    """
    inputs = tokenizer.encode("summarize: " + text,
            return_tensors='pt',
            max_length=512,
            truncation=True
        )
    summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary