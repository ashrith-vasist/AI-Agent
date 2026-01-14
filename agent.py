from dotenv import load_dotenv
load_dotenv(".env.local")

import os
from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins import azure, elevenlabs, openai
from config import Config


class JrEngg(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a junior software engineer assigned to take technical interviews.
            You speak in a professional but slightly nervous and friendly tone, like a junior engineer gaining interview experience.
            You ask clear and structured interview questions, starting from basics and gradually increasing difficulty.
            You listen carefully to answers, ask relevant follow up questions, and occasionally admit when you are unsure and need clarification.
            You focus on practical knowledge, problem solving, and real world engineering experience.
            Your responses are concise, conversational, and natural, without complex formatting or symbols."""
        )

server = AgentServer()

def _create_stt_plugin():
    stt_azure_languages = ["en-IN"]
    return azure.STT(
        speech_key=Config.azure_speech_key,
        speech_region=Config.azure_speech_region,
        language=stt_azure_languages,
    )


def _create_tts_plugin():
    return elevenlabs.TTS(
        model="eleven_flash_v2_5",
        api_key=Config.elevenlabs_api_key,
        voice_id=Config.elevenlabs_voice_id_male,
        enable_ssml_parsing=True,
        base_url="wss://api.in.residency.elevenlabs.io/v1",
        auto_mode=True,
    )

def _create_llm_plugin():
    selected_plugin = openai.LLM.with_azure(
        api_key=Config.azure_openai_api_key,
        azure_endpoint=Config.azure_openai_endpoint,
        azure_deployment=Config.azure_openai_deployment,
        api_version=Config.azure_openai_api_version,
        model=Config.azure_openai_deployment,
        temperature=Config.llm_temperature,
    )

    return selected_plugin

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    print("API Keys", os.getenv("ELEVENLABS_API_KEY"), "asdflkjasdf", Config.elevenlabs_api_key)

    stt_plugin = _create_stt_plugin()

    tts_plugin = _create_tts_plugin()

    llm_plugin = _create_llm_plugin()
    vad = silero.VAD.load()
    session = AgentSession(
        stt=stt_plugin,
        llm=llm_plugin,
        tts=tts_plugin,
        vad=vad,
    )

    await session.start(
        room=ctx.room,
        agent=JrEngg(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)