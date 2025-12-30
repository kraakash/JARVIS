import asyncio
import edge_tts

async def amain() -> None:
    voices = await edge_tts.VoicesManager.create()
    for v in voices.voices:
        if "hi-IN" in v["ShortName"]:
            print(f"ShortName: {v['ShortName']}, Gender: {v['Gender']}")

if __name__ == "__main__":
    asyncio.run(amain())
