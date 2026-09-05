#!/usr/bin/env python3
"""Import a supplied transcript or transcribe local audio with installed Whisper.

No hosted API, account or paid service is called. For audio, install openai-whisper
and ffmpeg first. The first run may download model weights. Text inputs always
work with Python alone. This tool does not perform speaker diarization.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--model', choices=['tiny', 'base', 'small', 'medium', 'large', 'turbo'], default='base')
    ap.add_argument('--language', help='Known audio language, e.g. en; omit for detection')
    args = ap.parse_args()
    if not args.input.is_file():
        ap.error('Input file does not exist')
    if args.out.exists():
        ap.error('Output exists; choose a new output filename')
    if args.input.suffix.lower() in ('.txt', '.md', '.srt', '.vtt'):
        content = args.input.read_text(encoding='utf-8')
        method = 'Imported supplied transcript; audio was not transcribed or verified'
    elif shutil.which('whisper') and shutil.which('ffmpeg'):
        with tempfile.TemporaryDirectory() as tmp:
            cmd = ['whisper', str(args.input.resolve()), '--model', args.model,
                   '--task', 'transcribe', '--output_format', 'json', '--output_dir', tmp, '--fp16', 'False']
            if args.language:
                cmd += ['--language', args.language]
            try:
                subprocess.run(cmd, check=True, timeout=1800)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                print('Transcription did not complete. Supply a transcript or use the bundled workshop transcript.', file=sys.stderr)
                return 1
            data = json.loads((Path(tmp) / (args.input.stem + '.json')).read_text())
            content = '\n'.join(f"[{s['start']:.1f}s - {s['end']:.1f}s] {s['text']}" for s in data['segments'])
            method = f'Local Whisper {args.model}; language={data.get("language")}; speaker identities not inferred'
    else:
        print('Audio transcription unavailable. Use a native transcription tool, install openai-whisper plus ffmpeg, '
              'or supply TXT/MD/SRT/VTT. Workshop fallback: workshop/data/oncology-mm/advisory-board-transcript.md', file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        stream.write(f'# Transcript for review\n\nSource: {args.input.name}\nMethod: {method}\n\n'
                     'Check medical names, numbers, negation and potential safety reports against the recording.\n\n' + content + '\n')
    print(f'Transcript saved: {args.out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
