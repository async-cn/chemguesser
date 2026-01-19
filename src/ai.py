from .config import Config
from openai import OpenAI

with open("config/prompt.md", mode="r", encoding="utf-8") as f:
    PROMPT = f.read()

if not PROMPT:
    raise Exception("Empty prompt provided")

if not Config.APIKEY:
    raise ValueError("API Key not found")
elif Config.APIKEY == "your_api_key":
    raise ValueError("请设置你自己的API Key")

client = OpenAI(api_key=Config.APIKEY, base_url=Config.BASEURL)

def request(problem:str, usermsg:str) -> str:
    """
    发送请求
    :param usermsg: 用户询问
    :return: AI回答
    """
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": PROMPT.replace("<problem>", problem)},
            {"role": "user", "content": usermsg},
        ],
        stream=False
    )
    return response.choices[0].message.content