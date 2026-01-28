from talker import talk

import asyncio
import json
import websockets

WS_URL = "ws://localhost:21213/"

async def connect():
    while True:
        try:
            print("🔌 Connecting...")
            async with websockets.connect(WS_URL) as websocket:
                print("✅ Connected")

                async for message in websocket:
                    try:
                        parsed_data = json.loads(message)
                        print("📩 Data received:")
                        print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
                    except json.JSONDecodeError:
                        print("⚠️ Received non-JSON message:")
                        print(message)

        except (websockets.exceptions.ConnectionClosedError,
                websockets.exceptions.InvalidURI,
                ConnectionRefusedError) as e:
            print("❌ Connection failed:", e)

        print("🔁 Reconnecting in 1 second...\n")
        await asyncio.sleep(1)



def main():
    pass # talk('macacada do diacho! vou fazer uma sopa pa nós!')

if __name__ == "__main__":
    main()
