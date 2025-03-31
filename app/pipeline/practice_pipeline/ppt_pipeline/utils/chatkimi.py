from openai import OpenAI

def chat_kimi(user_input:str,
              prompt:str,
              api_key:str="sk-lELm2XQafaLapPA1emJKG16qYWyLQFJhIK7gxZkGpZfNSwyg"):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(chat_kimi("你好",
                    "你是谁？"))
