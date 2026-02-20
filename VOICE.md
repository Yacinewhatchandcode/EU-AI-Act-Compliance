# Voice Interaction Guide for OpenClaw

## Why Voice Failed
Voice files on WhatsApp are often `.ogg` or `.opus` format. OpenClaw needs **FFmpeg** to convert these to a format the AI can transcribe.

## Fix Applied (Step Id: 2217)
1. **Enabled Plugin:** `talk-voice` added to `openclaw.json`.
2. **Installed FFmpeg:** via `winget`.

## How it works now
1. User sends voice note.
2. OpenClaw downloads `.ogg` file.
3. `talk-voice` plugin uses FFmpeg to convert it.
4. Whisper model transcribes it to text.
5. Agent processes the text request as usual.

## Troubleshooting
If voice still fails:
1. Ensure FFmpeg is in system PATH.
2. Restart the agent to reload PATH.
3. Check logs for "transcription failed".

## Commands
- **Send voice:** Just talk to the agent on WhatsApp.
- **Agent reply:** Agent replies with text (Voice response coming soon).
