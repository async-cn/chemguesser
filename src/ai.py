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

def request(prompt:str, usermsg:str, model:str=Config.MODEL) -> str:
    """
    发送请求
    :param prompt: 系统级提示词
    :param usermsg: 用户消息
    :return: AI回答
    """
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": usermsg},
        ],
        stream=False
    )
    return response.choices[0].message.content

def playerguess(problem:str, usermsg:str) -> str:
    """
    玩家猜测
    :param usermsg: 用户询问
    :return: AI回答
    """
    return request(PROMPT.replace("<problem>", problem), usermsg)