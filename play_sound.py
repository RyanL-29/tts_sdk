from logging import Logger
from typing import Generator, Dict, Any
import io
from pydub import AudioSegment
import pydub
import pyaudio
import pydub.utils
        
class PlaySound:
    def __init__(self, logger: Logger) -> None:
        logger.info("Initializing play sound")
        self.logger = logger
        AudioSegment.converter = "./lib/bin/ffmpeg.exe"
        AudioSegment.ffmpeg = "./lib/bin/ffmpeg.exe"
        pydub.utils.get_prober_name = lambda : "./lib/bin/ffprobe.exe"
    
    def play_stream(self, voice_clips: Generator[Dict[str, Any], None, None]):
        buffer = io.BytesIO()
        full_audio_buffer = io.BytesIO()
        segment_duration_ms = 3000
        stream = None
        p = pyaudio.PyAudio()
        try:
            self.logger.info("Voice stream started. Start playing sound")
            for message in voice_clips:
                if message["type"] == "audio":
                    buffer.write(message["data"])
                    full_audio_buffer.write(message["data"])
                    if buffer.tell() >= segment_duration_ms * 16:
                        buffer.seek(0)
                        audio_segment = AudioSegment.from_file(buffer, format="mp3")
                        
                        if stream is None:
                            stream = p.open(
                                format=p.get_format_from_width(audio_segment.sample_width),
                                channels=audio_segment.channels,
                                rate=audio_segment.frame_rate,
                                output=True
                            )
                        stream.write(audio_segment.raw_data)
                        buffer.seek(0)
                        buffer.truncate()
            
            buffer.seek(0)
            audio_segment = AudioSegment.from_file(buffer, format="mp3")
            with open("temp.mp3", "wb") as f:
                f.write(full_audio_buffer.getvalue())
            if stream is None:
                stream = p.open(
                    format=p.get_format_from_width(audio_segment.sample_width),
                    channels=audio_segment.channels,
                    rate=audio_segment.frame_rate,
                    output=True
                )
            stream.write(audio_segment.raw_data)
            buffer.seek(0)
            buffer.truncate()
                
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
                p.terminate()
            self.logger.info("Voice stream ended. Stop play sound")
                
            
    # def play_stream(self):
    #     # while self.sound_streaming or len(self.voice_clip) > 0:
    #     # if len(self.voice_clip) > 0:
    #     while len(self.voice_clip) < 1 and self.sound_streaming:
    #         time.sleep(0.01)
        
    #     if len(self.voice_clip) < 1 and not self.sound_streaming:
    #         return
    #     voice_bytes = self.voice_clip.pop(0)
    #     song = AudioSegment.from_file(io.BytesIO(voice_bytes), format="mp3")
    #     player_th = threading.Thread(target=play, args=(song, ))
    #     player_th.start()
    #     time.sleep((len(song) - 130) / 1000.0)
    #     self.play_stream()
                
    # def load_play_sound_stream(self, voice_clips: Generator[Dict[str, Any], None, None]):
    #     play_th = threading.Thread(target=self.play_stream)
    #     play_th.start()
    #     self.start_save_stream(voice_clips)
            
            
            
