import os
import asyncio
from groq import Groq
from dotenv import load_dotenv

from db import Database

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
db = Database()


async def ask_gpt(user_id: int, text: str) -> str:
    try:
        db.add_message(user_id, "user", text)

        history = db.get_history(user_id)

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"}
            ] + history
        )

        answer = response.choices[0].message.content

        db.add_message(user_id, "assistant", answer)

        return answer

    except Exception as e:
        print("GPT ERROR:", e)
        return "❌ Ошибка GPT"