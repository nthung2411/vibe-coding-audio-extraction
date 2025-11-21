# vibe-coding-audio-extraction

An offline audio extraction tool designed to extract audio from video files, optimized for handling large files (2GB+). This application runs entirely offline and uses FFmpeg for efficient processing.

## Features

- ✅ **Offline Processing**: No internet connection required, runs completely offline
- ✅ **Large File Support**: Optimized for files over 2GB
- ✅ **Multiple Formats**: Supports MP3, WAV, FLAC, AAC, OGG, M4A output formats
- ✅ **Quality Control**: Adjustable audio bitrate (128k, 192k, 256k, 320k, etc.)
- ✅ **Progress Reporting**: Shows progress during extraction for large files
- ✅ **Memory Efficient**: Uses streaming processing to handle large files without memory issues
- ✅ **Simple CLI**: Easy-to-use command-line interface

## Quick Start

### Prerequisites

1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **FFmpeg** - Required for audio extraction
   - Windows: `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd vibe-coding-audio-extraction
   ```

2. Verify FFmpeg is installed:
   ```bash
   ffmpeg -version
   ```

3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

### Usage

**Basic usage** (extracts to MP3 with default quality):
```bash
python audio_extractor.py video.mp4
```

**Specify output file and format**:
```bash
python audio_extractor.py video.mp4 -o output.mp3 -f mp3 -q 320k
```

**Extract as WAV (uncompressed)**:
```bash
python audio_extractor.py video.mp4 -f wav
```

**Extract as FLAC (lossless)**:
```bash
python audio_extractor.py video.mp4 -f flac
```

## Command Line Options

```
positional arguments:
  input_file            Path to the input video file

optional arguments:
  -h, --help            Show help message
  -o, --output OUTPUT   Path to the output audio file (auto-generated if not provided)
  -f, --format FORMAT   Output format: mp3, wav, aac, flac, ogg, m4a (default: mp3)
  -q, --quality QUALITY Audio bitrate, e.g., 128k, 192k, 256k, 320k (default: 192k)
  --no-progress         Hide progress information
```

## Examples

```bash
# Extract audio with default settings
python audio_extractor.py my_video.mp4

# High quality MP3
python audio_extractor.py my_video.mp4 -q 320k

# Extract as WAV with custom output name
python audio_extractor.py large_file.mkv -f wav -o audio_output.wav

# Lossless FLAC extraction
python audio_extractor.py video.mp4 -f flac -q 320k
```

## Supported Formats

### Input Formats
Any video format supported by FFmpeg:
- MP4, AVI, MKV, MOV, FLV, WebM, and many more

### Output Formats
- **MP3** - Compressed, widely compatible (default)
- **WAV** - Uncompressed, high quality
- **FLAC** - Lossless compression
- **AAC** - Modern compressed format
- **OGG** - Open source format
- **M4A** - Apple's audio format

## Large File Handling

This tool is specifically designed to handle large files efficiently:
- Uses FFmpeg's streaming processing (no need to load entire file into memory)
- Progress reporting for long operations
- No file size limitations
- Memory-efficient processing

## Project Structure

```
vibe-coding-audio-extraction/
├── audio_extractor.py    # Main extraction script
├── requirements.txt      # Python dependencies (minimal)
├── setup_guide.md       # Detailed setup instructions
└── README.md            # This file
```

## Requirements

- Python 3.8 or higher
- FFmpeg (must be installed separately)
- No additional Python packages required (uses only standard library)

## Troubleshooting

**"ffmpeg is not installed"**
- Install FFmpeg and ensure it's in your system PATH
- Verify with: `ffmpeg -version`

**"Input file not found"**
- Check the file path is correct
- Use absolute paths if needed

**Slow processing**
- Normal for large files (2GB+)
- Processing is CPU-intensive
- Be patient, especially for very large files

For more detailed setup instructions, see [setup_guide.md](setup_guide.md).

## License

This project is open source and available for learning purposes.

## Notes

- This application runs completely offline - no internet connection required
- Designed for local file processing, not for hosting as a web service
- Optimized for large files (2GB+) with efficient memory usage