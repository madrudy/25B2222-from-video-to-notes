# 25B2222-from-video-to-notes
This repo is a compilation of all my progress into the project of making an ai that turns youtube videos into short summarized notes.

Until now 2 milestones have been completed.

**Milestone 1: Converting Youtube video transcripts into readable .txt files**
This uses the library YouTubeTranscriptAPI which converts the transcript into a dict consisting of various segments. These segments are then merged and appropriate text processing is applied(removing timestamps, linebreaks, etc)

**Milestone 2: Building a summarization engine to summarize long texts(>10000 chars) into short readable text using huggingface models**
This uses HF transformers to convert large texts into overlapping chunks(because of token limits placed on models like bart-cnn or t5-small), then  summarizes these chunks independently. after that, the summarized chunks are merged and summarized again to create a final summary of overall text.

**Milestone 3: Building a frontend and backend integration for a website using python**
In this, I used streamlit, a python library made specifically to enable making websites using python. The code integrates my milestone 1 and milestone 2 codes to:
1. Make a custom txt file containing a clean and processed transcript for the youtube video.
2. Summarize said txt file using bart-cnn via chunking and modify the number of chunks generated and its size according to the users comfort.
3. Produce final summary of the video, as well as individual chunk summaries if the user wants.

To run the final code, simply make sure app.py, summarizer.py and youtube_extractor.py are in the same folder, and make sure to have downloaded the libraries mentioned in each code.


