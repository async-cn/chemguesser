# ChemGuesser 化学猜盐

![](https://img.shields.io/badge/License-MIT-blue)
![](https://img.shields.io/badge/Version-1.0-green)
![](https://img.shields.io/badge/Python-3.x-blue)

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

2. **安装依赖：** 进入 chemguess 目录，执行命令：

```bash
pip install -r requirements.txt
```

3. **配置环境：** 在找到 .env.example 文件，在其中设置模型、URL 以及 API Key：

```dotenv
BASEURL=https://api.deepseek.com
APIKEY=your_api_key
MODEL=deepseek-chat
```

配置完成后，将 .env.example 文件 **重命名为为 .env** 。

4. **启动游戏**：在 chemguess 目录下执行命令：

```bash
python run-terminal.py
```