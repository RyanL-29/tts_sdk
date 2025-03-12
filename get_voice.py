import edge_tts
import logging
from typing import Generator, Dict, Any, Union


class GetVoice:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def checkVoiceAvailable(self, voice) -> bool: 
        if voice in self.voice_list:
            return True
        else:
            return False
        
    def getVoiceClip(self, voice, text) -> Union[bool,  Generator[Dict[str, Any], None, None]]: 
        rate = "+0%"
        pitch = "+0Hz"
        if voice == "zh-HK-HiuGaaiNeural":
            rate = "+10%"
            pitch = "+8Hz"
        if voice == "zh-HK-HiuMaanNeural":
            pitch = "-2Hz"
        if isinstance(text, str) and len(text) > 0:
            try:
                # edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch).save_sync("./tts_out.mp3")
                voice_clips = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch).stream_sync()
                self.logger.info(f"Get voice clip success: {text}")
                return voice_clips
            except Exception as e:
                self.logger.error(f"Get voice clip failed: {e}")
                return False
        else:
            return False