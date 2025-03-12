import sys
from enum import Enum
from logging_manager import logger_manager
from word_processor import word_to_sub
from get_voice import GetVoice
from play_sound import PlaySound

support_voice_language = {
    "en-US": "en-US-AvaNeural",
    "zh-HK": "zh-HK-HiuGaaiNeural",
    "zh-CN": "zh-TW-HsiaoChenNeural"
}

SUPPORTED_VOICE_LANGUAGE = Enum("SUPPORTED_VOICE_LANGUAGE", names=support_voice_language)
    
def main():
    logger_handler = logger_manager()
    logger = logger_handler.initLogger()
    logger.info("TTY Service Initialized")

    language = str(sys.argv[1])
    text = str(sys.argv[2])
    
    if language not in SUPPORTED_VOICE_LANGUAGE._member_names_:
        logger.error("Language not supported")
        sys.exit(1)
    if len(text) < 1:
        logger.error("Text missing or empty is not allowed")
    
    logger.info(f"Start process {text} tts")
    text = word_to_sub(text, logger)
    voice_handler = GetVoice(logger=logger)
    voice_clips = voice_handler.getVoiceClip(text=text, voice=getattr(SUPPORTED_VOICE_LANGUAGE, language).value)
    if voice_clips:
        sound_player = PlaySound(logger=logger)
        sound_player.play_stream(voice_clips)
        # play_sound(logger=logger)
    
if __name__ == "__main__":
    main()



