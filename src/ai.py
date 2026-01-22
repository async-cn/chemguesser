from openai import OpenAI
from .config import Config
import json

with open("config/prompt.md", mode="r", encoding="utf-8") as f:
    PROMPT = f.read()
if not PROMPT:
    raise Exception("Empty prompt provided")

with open("config/elements.json", mode="r", encoding="utf-8") as f:
    ELEMENTS = json.load(f)
if not ELEMENTS:
    ELEMENTS = {}

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

class AIChat:
    """
    用于实现多轮AI对话，单轮对话请调用上文中更简单的request方法。
    """
    def __init__(self, model:str, system_prompt:str):
        self.model = model
        self.history = [{"role": "system", "content": system_prompt}]

    # noinspection PyTypeChecker
    def request(self, msg:str) -> str:
        self.history.append({"role": "user", "content": msg})
        response = client.chat.completions.create(
            model=self.model,
            messages=self.history,
            stream=False
        )
        self.history.append(response.choices[0].message)
        return response.choices[0].message.content

    def latest_response(self) -> str:
        return self.history[-1].content

def playerguess(problem:str, usermsg:str) -> str:
    """
    玩家猜测
    :param usermsg: 用户询问
    :return: AI回答
    """
    sysprompt = PROMPT.replace("[problem]", problem)

    elements_involved = False
    elements = []
    add_notices = False
    available_notices = {
        "akm": {
            'involved': False,
            'notice': "- 主族序数为1的金属元素是碱金属元素（氢元素除外）。"
        },
        "akem": {
            'involved': False,
            'notice': "- 主族序数为2的元素是碱土金属元素。"
        },
        "halogen": {
            'involved': False,
            'notice': '- 主族序数为7的元素是卤素（卤族元素）。'
        }
    }
    notices = []

    for char in problem:
        if char in ELEMENTS:
            if not elements_involved:
                elements_involved = True
                elements.append("参考元素信息: \n")
            e = ELEMENTS[char]
            line = f"- {char}: 原子序数：{e['index']}；相对原子质量：{e['molarmass']}；所在周期：{e['period']}；"
            if e['maingroup'] > 0:
                line += f"主族序数：{e['maingroup']}；"
                line += "是短周期主族元素；" if e['is_spmg'] else "不是短周期主族元素；"
                if e['maingroup'] in [1, 2, 7]:
                    add_notices = True
                    if e['maingroup'] == 1:
                        available_notices['akm']['involved'] = True
                    elif e['maingroup'] == 2:
                        available_notices['akem']['involved'] = True
                    elif e['maingroup'] == 7:
                        available_notices['halogen']['involved'] = True
            elements.append(line)

    sysprompt = sysprompt.replace("[elements]", '\n'.join(elements))

    if add_notices:
        notices.append("注意事项: \n")
        for value in available_notices.values():
            if value['involved']:
                notices.append(value['notice'])

    sysprompt = sysprompt.replace("[notice]", '\n'.join(notices) if add_notices else "")

    return request(sysprompt, usermsg)