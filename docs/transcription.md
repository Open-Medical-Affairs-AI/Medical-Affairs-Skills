# Audio and transcripts

**Workshop default:** the three therapeutic-area packs include advisory-board
transcripts. Use them immediately. Participants do not need audio software.

## With a supplied transcript

The agent can read MD, TXT, SRT or VTT directly. With Python it can preserve a
review copy and provenance:

```bash
python3 scripts/transcribe.py --input workshop/data/oncology-mm/advisory-board-transcript.md --out outputs/transcript.md
```

This imports text; it does not claim audio was transcribed or checked.

## With audio

Use an available host transcription capability when it is appropriate for the
recording. If running locally, the optional open-source path is Whisper:

1. Install Python and ffmpeg using the supported method for your computer.
2. Install Whisper in a dedicated environment: `python3 -m pip install openai-whisper`.
3. Run the helper below. Initial use downloads model weights; larger models need
   more memory and compute. Medical terminology still needs review.

```bash
python3 scripts/transcribe.py --input meeting.wav --out outputs/transcript.md --model base --language en
```

The helper uses a local command and does not send recordings to a hosted API.
It preserves segment timestamps, but does not identify speakers. Hosted audio
services may charge and require accounts; they are optional, not workshop prerequisites.

For actual recordings, confirm permission to record/process and the approved data
location. Do not commit recordings, secrets or actual patient details to the public
repository. Official installation and model guidance: [Whisper](https://github.com/openai/whisper).
