"""
Audio Extraction Tool
Extracts audio from video files, optimized for large files (2GB+)
"""

# Import the 'os' module - provides functions for interacting with the operating system
import os

# Import the 'sys' module - provides access to system-specific parameters and functions
# We use it to exit the program with error codes
import sys

# Import 'subprocess' - allows us to run external programs (like ffmpeg) from Python
import subprocess

# Import 'Path' from 'pathlib' - modern way to handle file paths in Python
# Path objects make it easier to work with file paths than strings
from pathlib import Path

# Import type hints - these help document what types of data functions expect/return
# Optional means the value can be the specified type OR None
# Tuple means a fixed-size collection of values
from typing import Optional, Tuple

# Import 'argparse' - helps create command-line interfaces
# It automatically parses command-line arguments and generates help messages
import argparse


# Define a class called AudioExtractor
# A class is like a blueprint for creating objects that have both data (attributes) and functions (methods)
class AudioExtractor:
    """Extracts audio from video files using ffmpeg."""
    
    # __init__ is a special method called a "constructor"
    # It runs automatically when you create a new AudioExtractor object
    # input_path: str means it expects a string (text) for the file path
    # Optional[str] = None means output_path can be a string OR None (not provided)
    # audio_format: str = "mp3" means it defaults to "mp3" if not specified
    # quality: str = "192k" means it defaults to "192k" if not specified
    def __init__(self, input_path: str, output_path: Optional[str] = None, 
                 audio_format: str = "mp3", quality: str = "192k"):
        """
        Initialize the AudioExtractor.
        
        Args:
            input_path: Path to the input video file
            output_path: Path for the output audio file (optional, auto-generated if not provided)
            audio_format: Output audio format (mp3, wav, aac, flac, etc.)
            quality: Audio bitrate (e.g., "192k", "320k", "128k")
        """
        # Convert the input_path string to a Path object
        # Path objects make it easier to work with file paths (join, get parent directory, etc.)
        # self.input_path means this is an attribute (data) that belongs to this object
        self.input_path = Path(input_path)
        
        # Convert audio_format to lowercase (e.g., "MP3" becomes "mp3")
        # .lower() is a string method that converts all letters to lowercase
        # This ensures format matching works regardless of how user types it
        self.audio_format = audio_format.lower()
        
        # Store the quality setting (bitrate) as an attribute
        self.quality = quality
        
        # Check if the input file actually exists on the filesystem
        # .exists() is a Path method that returns True if file exists, False otherwise
        # not self.input_path.exists() means "if the file does NOT exist"
        if not self.input_path.exists():
            # Raise an error if file doesn't exist
            # FileNotFoundError is a built-in Python exception type
            # f"..." is an f-string - it lets us insert variables into strings
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Generate output path if not provided
        # if output_path: means "if output_path is not None and not empty"
        if output_path:
            # User provided an output path, so use it
            # Convert string to Path object
            self.output_path = Path(output_path)
        else:
            # User didn't provide output path, so generate one automatically
            # self.input_path.parent gets the directory containing the input file
            # self.input_path.stem gets the filename without extension (e.g., "video" from "video.mp4")
            # f"{...}" creates a string with the stem and new extension
            # The / operator joins paths (works with Path objects)
            # Example: if input is "C:/Videos/video.mp4" and format is "mp3"
            # Result: "C:/Videos/video.mp3"
            self.output_path = self.input_path.parent / f"{self.input_path.stem}.{self.audio_format}"
    
    # Define a method (function) called check_ffmpeg
    # -> bool means this function returns a boolean (True or False)
    def check_ffmpeg(self) -> bool:
        """Check if ffmpeg is installed and available."""
        # try/except is Python's way of handling errors
        # Code in 'try' block runs, and if an error occurs, 'except' block handles it
        try:
            # subprocess.run() runs an external program (ffmpeg in this case)
            # ["ffmpeg", "-version"] is a list of command arguments
            # This is like running "ffmpeg -version" in the terminal
            subprocess.run(
                ["ffmpeg", "-version"],  # Command to run: ffmpeg with -version flag
                stdout=subprocess.DEVNULL,  # Don't capture standard output (discard it)
                stderr=subprocess.DEVNULL,  # Don't capture error output (discard it)
                check=True  # Raise an error if the command fails (returns non-zero exit code)
            )
            # If we get here, ffmpeg ran successfully, so it's installed
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If an error occurred, it means ffmpeg either:
            # - Returned an error code (CalledProcessError)
            # - Wasn't found in the system PATH (FileNotFoundError)
            # In either case, ffmpeg is not available
            return False
    
    # Method to convert file size to human-readable format (e.g., "2.5 GB")
    # Takes a Path object and returns a string
    def get_file_size(self, path: Path) -> str:
        """Get human-readable file size."""
        # path.stat() gets file information (size, modification time, etc.)
        # .st_size gets just the size in bytes (a number)
        size = path.stat().st_size
        
        # Loop through units from smallest to largest
        # for unit in [...] means "for each item in the list, assign it to 'unit' and run the code"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            # If size is less than 1024, we've found the right unit
            # 1024 is the number of bytes in a kilobyte (2^10)
            if size < 1024.0:
                # Return formatted string with 2 decimal places
                # f"{size:.2f}" formats the number with 2 decimal places
                # Example: 2048.5 becomes "2048.50"
                return f"{size:.2f} {unit}"
            # If size is >= 1024, divide by 1024 to convert to next unit
            # /= means "divide and assign" (same as size = size / 1024.0)
            size /= 1024.0
        
        # If file is larger than TB, return in petabytes (very unlikely but handles edge case)
        return f"{size:.2f} PB"
    
    # Main method that does the actual audio extraction
    # Returns a tuple: (success: True/False, message: string describing result)
    # show_progress defaults to True if not specified
    def extract_audio(self, show_progress: bool = True) -> Tuple[bool, str]:
        """
        Extract audio from the video file.
        
        Args:
            show_progress: Whether to show progress during extraction
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if ffmpeg is available before trying to use it
        # If check_ffmpeg() returns False, return early with an error message
        if not self.check_ffmpeg():
            # Return a tuple: (False for failure, error message)
            return False, "ffmpeg is not installed. Please install ffmpeg first."
        
        # Print information about what we're doing
        # print() displays text to the console
        # f"..." is an f-string that lets us insert variables
        print(f"Input file: {self.input_path}")
        # Call get_file_size() method to format the file size nicely
        print(f"Input size: {self.get_file_size(self.input_path)}")
        print(f"Output file: {self.output_path}")
        # .upper() converts string to uppercase (e.g., "mp3" becomes "MP3")
        print(f"Audio format: {self.audio_format.upper()}")
        print(f"Audio quality: {self.quality}")
        # "-" * 50 creates a string of 50 dashes (visual separator)
        print("-" * 50)
        
        # Build the ffmpeg command as a list of strings
        # Each string is an argument that will be passed to ffmpeg
        # Lists in Python use square brackets []
        cmd = [
            "ffmpeg",  # The program to run
            "-i", str(self.input_path),  # -i means "input file", convert Path to string
            "-vn",  # No video (don't include video stream, only audio)
            "-acodec", self._get_codec(),  # Audio codec (encoder) to use
            "-ab", self.quality,  # Audio bitrate (quality setting)
            "-y",  # Overwrite output file if it already exists (don't ask permission)
        ]
        
        # Add format-specific options based on the audio format
        # == checks if two values are equal
        if self.audio_format == "wav":
            # For WAV files, use PCM codec (uncompressed audio)
            # .extend() adds multiple items to the end of a list
            cmd.extend(["-acodec", "pcm_s16le"])
        # elif means "else if" - only checked if previous condition was False
        elif self.audio_format == "flac":
            # For FLAC files, use FLAC codec with compression level 5
            cmd.extend(["-acodec", "flac", "-compression_level", "5"])
        
        # Add progress reporting for large files
        # Only add these options if user wants to see progress
        if show_progress:
            # Add options to show progress information
            cmd.extend([
                "-progress", "pipe:1",  # Send progress to stdout (standard output)
                "-loglevel", "info"  # Set log level to info (shows progress messages)
            ])
        
        # Add the output file path as the last argument
        # .append() adds a single item to the end of a list
        # Convert Path object to string for subprocess
        cmd.append(str(self.output_path))
        
        # Wrap in try/except to catch any errors that occur
        try:
            # Print messages to inform user
            print("Starting audio extraction...")
            # \n creates a new line (blank line)
            print("This may take a while for large files. Please wait...\n")
            
            # Run ffmpeg with progress output
            # subprocess.Popen() starts a process and lets us interact with it
            # Unlike subprocess.run(), Popen doesn't wait for the process to finish
            process = subprocess.Popen(
                cmd,  # The command list we built earlier
                stdout=subprocess.PIPE,  # Capture standard output so we can read it
                stderr=subprocess.PIPE,  # Capture error output so we can read it
                universal_newlines=True,  # Treat output as text (strings) not bytes
                bufsize=1  # Line buffered (process output line by line)
            )
            
            # Monitor progress while ffmpeg is running
            if show_progress:
                # Read output line by line as it's generated
                # process.stdout is a file-like object we can read from
                for line in process.stdout:
                    # Check if this line contains time information
                    # "in" checks if a substring exists in a string
                    if "out_time_ms" in line:
                        # We could extract time info here, but for now just pass
                        # pass means "do nothing" (placeholder)
                        pass
                    # Print the line, stripping whitespace
                    # end='\r' means overwrite the same line (carriage return)
                    # This creates a "live" progress display
                    print(line.strip(), end='\r')
            
            # Wait for the process to finish and get all remaining output
            # communicate() waits for the process to complete
            # Returns a tuple: (stdout, stderr) - all the output text
            stdout, stderr = process.communicate()
            
            # Check if the process succeeded
            # returncode is 0 if successful, non-zero if there was an error
            if process.returncode == 0:
                # Success! Get the output file size
                output_size = self.get_file_size(self.output_path)
                # Print success message with separator
                print(f"\n{'=' * 50}")  # \n starts a new line, then 50 equals signs
                print("✓ Audio extraction completed successfully!")
                print(f"Output file: {self.output_path}")
                print(f"Output size: {output_size}")
                # Return success with a message
                return True, f"Successfully extracted audio to {self.output_path}"
            else:
                # Process failed - get error message
                # if stderr: means "if stderr is not empty"
                # This is a ternary-like expression: use stderr if it exists, otherwise use default message
                error_msg = stderr if stderr else "Unknown error occurred"
                # Return failure with error message
                return False, f"Extraction failed: {error_msg}"
                
        # Catch any unexpected errors
        # Exception is the base class for all errors in Python
        # as e means we can access the error object
        except Exception as e:
            # Convert the error to a string and return failure
            # str(e) converts the exception object to a readable string
            return False, f"Error during extraction: {str(e)}"
    
    # Private method (starts with _) to get the right codec for the audio format
    # Returns a string with the codec name
    def _get_codec(self) -> str:
        """Get the appropriate audio codec for the format."""
        # Create a dictionary (like a lookup table)
        # Keys are audio formats, values are the codec names ffmpeg uses
        # Dictionaries use curly braces {} and key: value pairs
        codec_map = {
            "mp3": "libmp3lame",  # MP3 uses LAME encoder
            "aac": "aac",  # AAC uses AAC encoder
            "wav": "pcm_s16le",  # WAV uses PCM (uncompressed)
            "flac": "flac",  # FLAC uses FLAC encoder
            "ogg": "libvorbis",  # OGG uses Vorbis encoder
            "m4a": "aac",  # M4A also uses AAC encoder
        }
        # .get() looks up a key in the dictionary
        # First argument is the key to look up (self.audio_format)
        # Second argument is the default value if key is not found
        # Returns "libmp3lame" if format is not in the dictionary
        return codec_map.get(self.audio_format, "libmp3lame")


# Define the main function - this is where program execution starts
# Functions are defined with 'def' keyword
def main():
    """Main CLI entry point."""
    # Create an ArgumentParser object
    # This object will handle parsing command-line arguments
    parser = argparse.ArgumentParser(
        description="Extract audio from video files (supports large files 2GB+)",  # Description shown in help
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Preserves formatting in help text
        epilog="""
Examples:
  # Extract audio with default settings (MP3, 192k)
  python audio_extractor.py video.mp4
  
  # Extract to specific output file
  python audio_extractor.py video.mp4 -o output.mp3
  
  # Extract as WAV with high quality
  python audio_extractor.py video.mp4 -f wav -q 320k
  
  # Extract as FLAC (lossless)
  python audio_extractor.py video.mp4 -f flac
        """  # Examples shown at the end of help message
    )
    
    # Add a positional argument (required, no dash prefix)
    # This is the input file - user must provide it
    parser.add_argument(
        "input_file",  # Argument name (no dash means it's required and positional)
        help="Path to the input video file"  # Description shown in help
    )
    
    # Add an optional argument for output file
    # -o is short form, --output is long form (both work the same)
    parser.add_argument(
        "-o", "--output",  # Short and long option names
        dest="output_file",  # Name of attribute in args object (args.output_file)
        help="Path to the output audio file (optional, auto-generated if not provided)"
    )
    
    # Add an optional argument for audio format
    parser.add_argument(
        "-f", "--format",  # User can type -f or --format
        dest="audio_format",  # Stored as args.audio_format
        default="mp3",  # If user doesn't specify, use "mp3"
        choices=["mp3", "wav", "aac", "flac", "ogg", "m4a"],  # Only allow these values
        help="Output audio format (default: mp3)"
    )
    
    # Add an optional argument for quality/bitrate
    parser.add_argument(
        "-q", "--quality",  # User can type -q or --quality
        dest="quality",  # Stored as args.quality
        default="192k",  # Default value if not specified
        help="Audio bitrate (default: 192k). Examples: 128k, 192k, 256k, 320k"
    )
    
    # Add a flag argument (no value, just True/False)
    parser.add_argument(
        "--no-progress",  # Flag name
        dest="show_progress",  # Stored as args.show_progress
        action="store_false",  # If flag is present, set to False; if absent, defaults to True
        help="Hide progress information"
    )
    
    # Parse the command-line arguments
    # This reads sys.argv (command-line arguments) and creates an args object
    # args.input_file, args.output_file, etc. contain the parsed values
    args = parser.parse_args()
    
    # Try to run the extraction
    try:
        # Create an AudioExtractor object
        # This calls the __init__ method we defined earlier
        # We pass the parsed command-line arguments
        extractor = AudioExtractor(
            input_path=args.input_file,  # Get input file from parsed arguments
            output_path=args.output_file,  # Get output file (may be None)
            audio_format=args.audio_format,  # Get format (defaults to "mp3")
            quality=args.quality  # Get quality (defaults to "192k")
        )
        
        # Call the extract_audio method
        # It returns a tuple: (success: bool, message: str)
        # We "unpack" it into two variables: success and message
        success, message = extractor.extract_audio(show_progress=args.show_progress)
        
        # Check if extraction was successful
        if success:
            # Print success message to standard output
            print(message)
            # Exit program with code 0 (success)
            # sys.exit() stops the program immediately
            sys.exit(0)
        else:
            # Extraction failed
            # Print error to stderr (standard error stream)
            # file=sys.stderr means send output to error stream, not normal output
            print(f"Error: {message}", file=sys.stderr)
            # Exit with code 1 (error/failure)
            sys.exit(1)
            
    # Handle specific error: file not found
    # except catches errors that occur in the try block
    except FileNotFoundError as e:
        # e contains the error object
        # Print error message to stderr
        print(f"Error: {e}", file=sys.stderr)
        # Exit with error code
        sys.exit(1)
    # Handle user cancellation (Ctrl+C)
    except KeyboardInterrupt:
        # User pressed Ctrl+C to cancel
        print("\n\nExtraction cancelled by user.")
        # Exit with error code (user cancelled)
        sys.exit(1)
    # Catch any other unexpected errors
    except Exception as e:
        # Print the error message
        print(f"Unexpected error: {e}", file=sys.stderr)
        # Exit with error code
        sys.exit(1)


# This is a special Python idiom
# __name__ is a built-in variable that Python sets automatically
# When you run a Python file directly, __name__ is set to "__main__"
# When you import a file as a module, __name__ is set to the module name
# This check means: "only run main() if this file is being run directly, not imported"
if __name__ == "__main__":
    # Call the main function to start the program
    main()

