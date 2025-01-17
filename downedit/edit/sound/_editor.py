from moviepy.editor import *

from ...edit.base import Editor

class SoundEditor(Editor):
    def __init__(self, input_path = None, output_path = None):
        super().__init__(input_path, output_path)
        self.audio_clip = AudioFileClip(self.input_path)

    def volume(self, volume=0.5):
        """Changes the volume of an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            volume (float, optional): Volume level (default: 0.5).
        """
        self.audio_clip = self.audio_clip.volumex(volume)
        return self
    
    def fade_in(self, duration=2):
        """Fades in an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            duration (float, optional): Fade-in duration in seconds (default: 2).
        """
        self.audio_clip = self.audio_clip.audio_fadein(duration)
        return self
    
    def fade_out(self, duration=2):
        """Fades out an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            duration (float, optional): Fade-out duration in seconds (default: 2).
        """
        self.audio_clip = self.audio_clip.audio_fadeout(duration)
        return self
    
    def render(
        self
    ):
        """
        Writes the modified audio to the specified output path.
        """
        try:
            self.audio_clip.write_audiofile(
                self.output_path,
                verbose=False,
                logger=None
            )
        finally:
            self.audio_clip.close()