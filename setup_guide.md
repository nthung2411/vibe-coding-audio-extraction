# Setup Guide

## Prerequisites

### 1. Install Python
- Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### 2. Install FFmpeg
FFmpeg is required for audio extraction. It's a powerful multimedia framework.

#### Windows:
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or use a package manager:
   - **Using Chocolatey**: `choco install ffmpeg`
   - **Using Scoop**: `scoop install ffmpeg`
   - **Manual**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

#### macOS:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd vibe-coding-audio-extraction
   ```

3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. No Python packages need to be installed (the script uses only standard library)

## Usage

### Basic Usage
```bash
python audio_extractor.py video.mp4
```

This will create `video.mp3` in the same directory as the input file.

### Advanced Usage

#### Specify output file:
```bash
python audio_extractor.py video.mp4 -o output.mp3
```

#### Change audio format:
```bash
# Extract as WAV
python audio_extractor.py video.mp4 -f wav

# Extract as FLAC (lossless)
python audio_extractor.py video.mp4 -f flac

# Extract as AAC
python audio_extractor.py video.mp4 -f aac
```

#### Change audio quality:
```bash
# High quality (320k)
python audio_extractor.py video.mp4 -q 320k

# Medium quality (192k - default)
python audio_extractor.py video.mp4 -q 192k

# Lower quality, smaller file (128k)
python audio_extractor.py video.mp4 -q 128k
```

#### Combine options:
```bash
python audio_extractor.py large_video.mp4 -f wav -q 320k -o high_quality_audio.wav
```

## Supported Formats

### Input Formats
Any video format supported by FFmpeg:
- MP4, AVI, MKV, MOV, FLV, WebM, and many more

### Output Formats
- MP3 (default)
- WAV (uncompressed)
- FLAC (lossless compression)
- AAC
- OGG
- M4A

## Large File Support

This tool is optimized for large files (2GB+):
- Uses FFmpeg's efficient streaming processing
- No file size limits
- Progress reporting for long operations
- Memory-efficient processing

## Troubleshooting

### "ffmpeg is not installed"
- Make sure FFmpeg is installed and available in your PATH
- Verify with: `ffmpeg -version`

### "Input file not found"
- Check that the file path is correct
- Use absolute paths if relative paths don't work

### Extraction is slow
- This is normal for large files
- The process is CPU-intensive
- Be patient, especially for files over 2GB

### Out of memory errors
- FFmpeg handles large files efficiently, but if you encounter issues:
  - Close other applications
  - Process files one at a time
  - Consider using a lower quality setting

