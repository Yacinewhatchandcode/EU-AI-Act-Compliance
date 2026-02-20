"""
Local Speech-to-Text Transcription for OpenClaw
Uses faster-whisper (free, local, no API key needed)
First run downloads the model (~150MB for 'base', ~1GB for 'medium')
"""
import sys
import os

def transcribe(audio_path, model_size="base"):
    """Transcribe an audio file to text using local Whisper."""
    from faster_whisper import WhisperModel
    
    if not os.path.exists(audio_path):
        print(f"Error: File not found: {audio_path}")
        return None
    
    # Use CPU (works on all machines). Change to "cuda" if you have NVIDIA GPU.
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    text = " ".join([seg.text.strip() for seg in segments])
    
    print(f"[Language: {info.language} | Confidence: {info.language_probability:.1%}]")
    print(text)
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file> [model_size]")
        print("  model_size: tiny, base (default), small, medium, large-v3")
        print("  Larger = more accurate but slower")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    transcribe(audio_file, model)
