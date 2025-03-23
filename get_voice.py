import edge_tts
import logging
from typing import Generator, Dict, Any, Union, AsyncGenerator, Optional
from edge_tts.typing import TTSChunk


class GetVoice:
    def __init__(self, logger: Optional[logging.Logger] = None):
        if not logger:
            self.logger = logging.Logger('temp_getvoice_logger')
        else:
            self.logger = logger
        
    def getVoiceClip(self, voice, text) -> Union[bool, Generator[TTSChunk, None, None]]: 
        rate = "+0%"
        pitch = "+0Hz"
        if voice == "zh-HK-HiuGaaiNeural":
            rate = "+10%"
            pitch = "+8Hz"
        if voice == "zh-HK-HiuMaanNeural":
            pitch = "-2Hz"
        if isinstance(text, str) and len(text) > 0:
            try:
                voice_clips = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch).stream_sync()
                self.logger.info(f"Get voice clip success: {text}")
                return voice_clips
            except Exception as e:
                self.logger.error(f"Get voice clip failed: {e}")
                return False
        else:
            return False