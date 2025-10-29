import os
from openai import OpenAI
from dotenv import load_dotenv

# 🔐 API kalitni yuklash
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 💬 Chat funksiyasi
def chat():
    print("🤖 AI bilan suhbat (chiqish uchun 'exit' yozing):\n")
    history = []

    while True:
        user_input = input("Siz: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Xayr!")
            break

        # 🧠 OpenAI chaqiruv
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # yoki "gpt-4o-mini"
            messages=[
                {"role": "system", "content": "Siz foydalanuvchiga yordam beruvchi AI assistentsiz."},
                *history,
                {"role": "user", "content": user_input},
            ]
        )

        reply = completion.choices[0].message.content
        print(f"AI: {reply}\n")

        # Tarixni saqlaymiz (suhbat konteksti uchun)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat()






