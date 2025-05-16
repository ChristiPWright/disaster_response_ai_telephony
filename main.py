#TODO: call end logic

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from utils import load_prompt

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=load_prompt('prompt.yaml'),
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=cartesia.TTS(),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession()
    agent = Assistant()

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVCTelephony(), 
        ),
    )

    await session.generate_reply(
        instructions="We are going to get you help; but please know if you are having an emergency hang up and call 911."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,

        # agent_name is required for explicit dispatch
        agent_name="inbound-agent"
    ))