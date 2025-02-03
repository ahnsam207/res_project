import openai
import os

api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

messages = [
    {"role" : "user", "content" : "한글은 언제 만들어졌나요?"}
]

response = openai.chat.completions.create(
    model = "gpt-3.5-turbo", # GPT 모델 선택
    messages = messages, # 전달할 메시지 지정
    temperature = 0.8, # 완성의 다양성을 조절하는 온도 설정
    max_tokens = 1000, # 응답 최대 토큰 수 지정
    n=3 # 응답 개수 지정
)

# assistant_reply = response.choices[0].message.content
# print(assistant_reply)

print("응답 1" , response.choices[0].message.content)
print("응답 2" , response.choices[1].message.content)
print("응답 3" , response.choices[2].message.content)