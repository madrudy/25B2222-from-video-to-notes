"""
Milestone 3: Complete YouTube to Notes App
Integrating:
- Milestone 1: YOUR YouTube transcript extraction (from main.py)
- Milestone 2: YOUR HuggingFace summarization (from summarizer.py)
- Milestone 3: Streamlit UI
"""

import streamlit as st
import sys
import os

# Import YOUR Milestone 1 code
from youtube_extractor import get_youtube_transcript, extract_video_id

# Import YOUR Milestone 2 code
from summarizer import summarize_long_text, chunk_text

# Page config
st.set_page_config(
    page_title="YouTube to Notes - AI Summarizer",
    page_icon="📹",
    layout="wide"
)


def main():
    st.title("📹 YouTube Video to Notes")
    st.markdown("**Complete Integration: Milestones 1 + 2 + 3**")
    st.caption("Using YOUR code: YouTube extraction + HuggingFace BART summarization")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.markdown("### Chunking Settings")
        chunk_size = st.slider("Chunk Size (characters)", 800, 2000, 1200, step=100)
        overlap = st.slider("Overlap Size (characters)", 50, 300, 150, step=50)
        
        st.divider()
        
        st.markdown("### Display Options")
        show_chunks = st.checkbox("Show intermediate chunks", value=False)
        show_chunk_summaries = st.checkbox("Show chunk summaries", value=False)
        
        st.divider()
        
        st.markdown("### 🎯 Milestone Progress")
        st.success("✅ M1: YouTube Transcript Extraction")
        st.success("✅ M2: HuggingFace BART Summarization")
        st.success("✅ M3: Streamlit UI Integration")
        
        st.divider()
        
        st.markdown("### 📊 Model Info")
        st.info("**Model**: facebook/bart-large-cnn\n\n**Method**: Hierarchical chunking + summarization")
    
    # Main input area
    st.header("📥 Input Your Content")
    
    # Tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["🎥 YouTube URL", "📝 Paste Text", "📄 Upload File"])
    
    input_text = None
    source_info = None
    
    # TAB 1: YouTube URL (YOUR MILESTONE 1)
    with tab1:
        st.markdown("### Extract transcript from YouTube video")
        st.caption("Uses your Milestone 1 code (YouTube Transcript API)")
        
        youtube_url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=... or https://youtu.be/...",
            help="Paste any YouTube video URL"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            extract_btn = st.button("📥 Extract & Summarize", type="primary", key="yt_btn")
        
        if extract_btn:
            if not youtube_url:
                st.error("❌ Please enter a YouTube URL")
            else:
                with st.spinner("📥 Extracting transcript from YouTube..."):
                    try:
                        # YOUR MILESTONE 1 CODE
                        raw_text, video_id, segments = get_youtube_transcript(youtube_url)
                        
                        input_text = raw_text
                        source_info = {
                            'type': 'YouTube',
                            'url': youtube_url,
                            'video_id': video_id,
                            'segments': len(segments)
                        }
                        
                        st.success(f"✅ Transcript extracted successfully!")
                        st.info(f"**Video ID**: {video_id} | **Segments**: {len(segments)} | **Words**: {len(raw_text.split())}")
                        
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
                        st.info("Make sure the video has English captions/subtitles available.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # TAB 2: Manual text input
    with tab2:
        st.markdown("### Paste or type your text")
        user_text = st.text_area(
            "Enter text to summarize:",
            height=250,
            placeholder="Paste your long-form content here...\n\nMinimum 100 characters recommended for best results.",
            help="For best results, use text longer than 500 characters"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            text_btn = st.button("📝 Summarize Text", type="primary", key="text_btn")
        
        if text_btn:
            if not user_text or len(user_text.strip()) < 100:
                st.error("❌ Please enter at least 100 characters")
            else:
                input_text = user_text.strip()
                source_info = {
                    'type': 'Manual Text',
                    'length': len(input_text)
                }
    
    # TAB 3: File upload
    with tab3:
        st.markdown("### Upload a text file")
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt', 'md'],
            help="Upload a .txt or .md file"
        )
        
        if uploaded_file:
            st.info(f"📄 File: **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            file_btn = st.button("📄 Summarize File", type="primary", key="file_btn", 
                                disabled=uploaded_file is None)
        
        if file_btn and uploaded_file:
            try:
                content = uploaded_file.read().decode('utf-8')
                if len(content.strip()) < 100:
                    st.error("❌ File content too short (minimum 100 characters)")
                else:
                    input_text = content.strip()
                    source_info = {
                        'type': 'File',
                        'filename': uploaded_file.name,
                        'size': uploaded_file.size
                    }
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    # ============= PROCESS AND DISPLAY RESULTS =============
    if input_text:
        st.divider()
        st.header("🔄 Processing...")
        
        # Show input stats
        word_count = len(input_text.split())
        char_count = len(input_text)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Characters", f"{char_count:,}")
        col2.metric("Words", f"{word_count:,}")
        col3.metric("Estimated Chunks", max(1, char_count // chunk_size))
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Chunking (YOUR M2 CODE)
            status_text.text("Step 1/3: Chunking text...")
            progress_bar.progress(0.1)
            
            chunks = chunk_text(input_text, chunk_size=chunk_size, overlap=overlap)
            num_chunks = len(chunks)
            
            status_text.text(f"Step 1/3: Created {num_chunks} chunks ✓")
            progress_bar.progress(0.3)
            
            # Step 2: Summarization (YOUR M2 CODE)
            status_text.text("Step 2/3: Summarizing chunks with BART model...")
            progress_bar.progress(0.4)
            
            # Use YOUR exact function
            chunk_summaries, final_summary = summarize_long_text(input_text)
            
            progress_bar.progress(0.9)
            status_text.text("Step 3/3: Finalizing summary ✓")
            
            progress_bar.progress(1.0)
            status_text.text("✅ Processing complete!")
            
            # ============= DISPLAY RESULTS =============
            st.divider()
            st.header("📊 Results")
            
            # Source info
            if source_info:
                info_text = f"**Source**: {source_info['type']}"
                if source_info['type'] == 'YouTube':
                    info_text += f" | Video ID: `{source_info['video_id']}`"
                elif source_info['type'] == 'File':
                    info_text += f" | File: `{source_info['filename']}`"
                st.caption(info_text)
            
            # Main Summary
            st.subheader("📄 Final Summary")
            st.markdown(f"**{final_summary}**")
            
            # Key Points (extract from summary)
            st.subheader("🔹 Key Points")
            sentences = [s.strip() + "." for s in final_summary.split(".") if s.strip()]
            for i, sentence in enumerate(sentences[:5], 1):
                st.markdown(f"{i}. {sentence}")
            
            # Statistics
            st.divider()
            st.subheader("📈 Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Original Words", f"{word_count:,}")
            col2.metric("Summary Words", f"{len(final_summary.split()):,}")
            compression = round((1 - len(final_summary.split()) / word_count) * 100, 1)
            col3.metric("Compression", f"{compression}%")
            col4.metric("Chunks Processed", num_chunks)
            
            # Show processing details (optional)
            if show_chunks or show_chunk_summaries:
                st.divider()
                st.subheader("🔍 Processing Details")
                
                if show_chunks:
                    with st.expander(f"📦 View {num_chunks} Text Chunks"):
                        for i, chunk in enumerate(chunks, 1):
                            st.markdown(f"**Chunk {i}/{num_chunks}** ({len(chunk)} chars, {len(chunk.split())} words)")
                            st.text_area(f"Chunk {i}", chunk, height=100, key=f"chunk_{i}")
                            st.divider()
                
                if show_chunk_summaries:
                    with st.expander(f"📝 View {len(chunk_summaries)} Chunk Summaries"):
                        for i, summary in enumerate(chunk_summaries, 1):
                            st.markdown(f"**Summary {i}/{len(chunk_summaries)}**")
                            st.info(summary)
                            st.divider()
            
            # Download options
            st.divider()
            st.subheader("💾 Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Full notes
                full_notes = f"""YouTube to Notes - Complete Summary
{'='*50}

SOURCE: {source_info['type'] if source_info else 'Unknown'}
ORIGINAL LENGTH: {word_count} words
SUMMARY LENGTH: {len(final_summary.split())} words
COMPRESSION: {compression}%

{'='*50}
FINAL SUMMARY
{'='*50}

{final_summary}

{'='*50}
KEY POINTS
{'='*50}

""" + "\n".join([f"{i}. {s}" for i, s in enumerate(sentences[:5], 1)]) + f"""

{'='*50}
CHUNK SUMMARIES
{'='*50}

""" + "\n\n".join([f"[Chunk {i}]\n{s}" for i, s in enumerate(chunk_summaries, 1)]) + f"""

{'='*50}
ORIGINAL TEXT
{'='*50}

{input_text}
"""
                
                st.download_button(
                    label="📥 Download Complete Notes",
                    data=full_notes,
                    file_name="youtube_notes_complete.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Summary only
                summary_only = f"""SUMMARY

{final_summary}

KEY POINTS:
""" + "\n".join([f"{i}. {s}" for i, s in enumerate(sentences[:5], 1)])
                
                st.download_button(
                    label="📄 Download Summary Only",
                    data=summary_only,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error during processing: {str(e)}")
            st.info("💡 Try adjusting the chunk size in the sidebar or using shorter text.")
            
            # Show error details in expander
            with st.expander("🔍 Error Details"):
                import traceback
                st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
