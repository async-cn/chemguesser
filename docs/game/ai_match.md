# AI 对战

规则与匹配对战基本一致，但对手是使用.env中BATTLE_MODEL模型的AI。AI会模拟人类玩家的行为与当前玩家进行对战。

特别地，AI对战结束后玩家的ELO等级分不会发生变化。

注意：AI对手（即AI模拟的玩家）在对战过程中可能需要用到多轮对话，但ai请求的api是“无状态”的，即不会保留上下文，所以多轮对话时每次向AI对手发送其猜测的回答都需要拼接之前每一轮的对话信息（“user”和“assistant”，其中“assistant”为AI对手）。

以下是一个通过上下文拼接进行多轮对话的例子：

```python
from openai import OpenAI
client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 1: {messages}")

# Round 2
messages.append({"role": "user", "content": "What is the second?"})
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 2: {messages}")
```