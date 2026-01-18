from os import statvfs_result
import os

class Config:
    #livekit
    livekit_api_key = os.getenv("LIVEKIT_API_KEY")
    livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")
    livekit_url = os.getenv("LIVEKIT_URL")

    #Azure stt
    azure_speech_region: str = os.getenv("AZURE_SPEECH_REGION")
    azure_speech_key: str = os.getenv("AZURE_SPEECH_KEY")

    #ElevenLabs tts
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY")
    elevenlabs_voice_id_male: str = os.getenv("ELEVENLABS_VOICE_ID_FEMALE")
    elevenlabs_voice_id_female: str = os.getenv("ELEVENLABS_VOICE_ID_FEMALE")

    #Azure llm
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    llm_temperature: float = 0.0

