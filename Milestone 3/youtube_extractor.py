from youtube_transcript_api import YouTubeTranscriptApi
import json


def extract_video_id(url):
    if url.startswith("https://youtu.be/"):
        video_id = url.split("/")[-1]
    elif url.startswith("https://www.youtube.com/watch?v="):
        video_id = url.split("v=")[-1].split("&")[0]
    else:
        raise ValueError("Invalid YouTube URL format.")
    
    return video_id


def get_youtube_transcript(url):
    # Extract video ID
    video_id = extract_video_id(url)
    
    # Fetch transcript
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    
    segments = None
    
    # Find English transcript
    for transcript in transcript_list:
        if transcript.language_code == 'en':
            segments = transcript.fetch()
            break
    
    if segments is None:
        raise ValueError("No English transcript available.")
    
    # Merge segments into raw text
    raw_text = ""
    for segment in segments:
        raw_text += segment.text + " "
    
    # Clean the text (YOUR EXACT CLEANING LOGIC)
    raw_text = raw_text.strip().replace("\n", " ")  # remove line breaks
    
    while "  " in raw_text:  # remove double spaces
        raw_text = raw_text.replace("  ", " ")
    
    for punct in [".", ",", "!", "?", ";", ":"]:  # remove spaces before punctuations
        raw_text = raw_text.replace(" " + punct, punct + " ")
    
    return raw_text, video_id, segments


def save_transcript_files(raw_text, video_id, segments, output_dir="."):
    import os
    
    # Save to txt
    txt_path = os.path.join(output_dir, "transcript.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(raw_text)
    
    # Prepare JSON data
    json_segments = []
    for segment in segments:
        json_segments.append({
            "text": segment.text,
            "start": segment.start,
            "duration": segment.duration
        })
    
    data = {
        "video_id": video_id,
        "language": "en",
        "transcript": raw_text,
        "segments": json_segments
    }
    
    # Save to JSON
    json_path = os.path.join(output_dir, "transcript.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return txt_path, json_path