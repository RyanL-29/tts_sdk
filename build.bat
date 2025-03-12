@REM pyinstaller --noconfirm --distpath ./ --onefile --console --clean ./tts_sdk.py
nuitka --follow-imports --onefile --output-dir=dist --output-filename=tts_sdk.exe ./tts_sdk.py