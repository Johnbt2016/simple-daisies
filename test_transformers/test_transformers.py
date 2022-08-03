from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import sentencepiece
from transformers import pipeline

# tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
# model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

summarizer = pipeline("summarization", model="philschmid/distilbart-cnn-12-6-samsum")

def generate_summary(text, min_length = 80, max_length=150):
    
    

    conversation = '''Jeff: Can I train a 🤗 Transformers model on Amazon SageMaker? 
    Philipp: Sure you can use the new Hugging Face Deep Learning Container. 
    Jeff: ok.
    Jeff: and how can I get started? 
    Jeff: where can I find documentation? 
    Philipp: ok, ok you can find everything here. https://huggingface.co/blog/the-partnership-amazon-sagemaker-and-hugging-face                                           
    '''
    out = summarizer(conversation)

    return out