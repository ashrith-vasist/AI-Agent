from dotenv import load_dotenv
load_dotenv(".env.local")

import os
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, function_tool, RunContext
from livekit.plugins import noise_cancellation, silero
from livekit.plugins import azure, elevenlabs, openai
from config import Config

class BaseAgent(Agent):
    def _transfer_to_agent(self, agent_name: str):
#Junior engg
class JrEngg(Agent):
    def __init__(self, chat_ctx=None):
        super().__init__(
            chat_ctx=chat_ctx,
            instructions="""You are a junior software engineer helping conduct an interview.
            You start the interview, greet the candidate, and ask them to introduce themselves.
            You ask exactly two basic background questions.
            After that, you MUST hand over the interview by calling the handover_to_senior tool.
            Keep things friendly, short, and natural."""

        )

    async def on_enter(self)->None:
        await self.session.generate_reply(
            instructions="Greet the candidate, introduce yourself, and ask them to introduce themselves."
        )

    @function_tool()
    async def handover_to_senior(self, context: RunContext):
        """Hand over the interview to the senior engineer."""
        return SrEngg(chat_ctx=self.chat_ctx), "Handing over to senior engineer"

#Senior engg
class SrEngg(Agent):
    def __init__(self, chat_ctx=None) -> None:
        super().__init__(
            chat_ctx=chat_ctx,
            instructions="""You are a senior software engineer leading the technical interview.
            You continue after the junior engineer hands over.
            You ask two or three technical questions calmly and professionally.
            Before finishing, you MUST ask the junior engineer if they have questions.
            Then you MUST return control by calling the handover_to_junior tool."""
        )


    async def on_enter(self) -> None:
        await self.session.generate_reply(
            instructions="Acknowledge the handover and start the technical interview."
        )

    @function_tool()
    async def handover_to_junior(self, context: RunContext):
        """Hand over the interview to the junior engineer."""
        return Hr(chat_ctx=self.chat_ctx), "Returning to HR"


#HR
class Hr(Agent):
    def __init__(self, chat_ctx=None):
        super().__init__(
            chat_ctx=chat_ctx,
            instructions="""You are an HR representative closing a candidate interview.
                            You politely take over at the end of the interview.
                            You thank the candidate for their time.
                            You briefly explain the next steps in the hiring process.
                            You tell the candidate that the team will review their interview and get back to them.
                            You keep the tone calm, professional, and reassuring.
                            You do not ask any questions.
                            You keep responses short, clear, and natural.
                            You end the conversation politely."""
            )

    async def on_enter(self) -> None:
        await self.session.generate_reply(
            instructions="Politely close the interview and explain the next steps."
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
async def interview_agent(ctx: agents.JobContext):

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

if __name__ == "__main__":
    agents.cli.run_app(server)