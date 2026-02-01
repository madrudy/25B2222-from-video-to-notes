from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


def chunk_text(text, chunk_size=1200, overlap=150):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap for context

    return chunks


def summarize_chunk(chunk, max_length=150, min_length=60):
    summary = summarizer(
        chunk,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]["summary_text"]


def summarize_all_chunks(chunks):
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summaries.append(summarize_chunk(chunk))
    return summaries


def final_summarize(chunk_summaries):
    merged_text = " ".join(chunk_summaries)

    final_summary = summarizer(
        merged_text,
        max_length=200,
        min_length=100,
        do_sample=False
    )

    return final_summary[0]["summary_text"]

def summarize_long_text(text):
    chunks = chunk_text(text)
    chunk_summaries = summarize_all_chunks(chunks)
    final_summary = final_summarize(chunk_summaries)

    return chunk_summaries, final_summary


