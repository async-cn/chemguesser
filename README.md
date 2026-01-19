# ChemGuesser 化学猜盐

> [!NOTE]
> 
> 开发中，敬请期待。
> 
> 后续开发计划：UI界面、自定义题库、多人竞技、有机模式等。

一款有点好玩的化学猜盐小游戏。

## 使用方法

1. **克隆仓库：** 执行以下命令：

```bash
git clone https://github.com/async-cn/chemguesser.git
```

2. **配置环境：** 进入 chemguess 目录，找到 .env.example 文件，配置模型、URL 以及 API Key：

```dotenv
BASEURL=https://api.deepseek.com
APIKEY=your_api_key
MODEL=deepseek-chat
```

配置完成后，将 .env.example 文件 **重命名为为 .env** 。

3. **启动游戏**：在 chemguess 目录下执行命令：

```bash
python run-terminal.py
```