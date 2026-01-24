<div align="center">
    <img src="https://www.chemguesser.com/static/chemguesser-logo.png" width="100" height="100"/>
    <h1 style="margin-top: -15px">ChemGuesser 化学猜盐</h1>
    <p>一款有点好玩的化学猜盐小游戏</p>
    <img src="https://img.shields.io/badge/License-MIT-blue">
    <img src="https://img.shields.io/badge/Version-1.0-green">
    <img src="https://img.shields.io/badge/Python-3.x-blue">
</div>

> [!NOTE]
>
> TODO: 
> 
> 详细开发计划见[docs/dev_plan.md](docs/dev_plan.md)
> 
>  - 优化题库，将元素和物质信息直接嵌入题库。
>  - 制作有机题库。
>  - 开发AI对战模式。
>  - 开发题目信息统计，优化题库难度划分机制。
>  - 使用 Redis 实现验证码，优化性能。
>  - 开发PVP模式。

## 使用方法

1. **克隆仓库：** 执行以下命令：

```bash
git clone https://github.com/async-cn/chemguesser.git
```

2. **安装依赖：** 进入 chemguess 目录，执行命令：

```bash
pip install -r requirements.txt
```

3. **配置环境：** 在找到 .env.example 文件，在其中设置模型、URL、API Key等一系列配置：

```dotenv
BASEURL=https://api.deepseek.com
APIKEY=your_api_key
MODEL=deepseek-chat
ROOT_KEY=your_custom_root_key_which_can_be_set_to_anything_you_like
SMTP_SERVER=smtp.qq.com
SMTP_PORT=465
SMTP_ADDR=your_email_addr
SMTP_KEY=your_smtp_key
BATTLE_MODEL=deepseek-reasoner
BATTLE_CONFIRM_TIME_LIMIT=45
BATTLE_DAMAGE_BASE=200
BATTLE_DAMAGE_SCALE_INCREASEMENT=0.25
WEBSITE_ADDR=localhost
WEBSITE_PORT=2300
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=sqlite:///chemguesser.db
```
> [!NOTE]
> 
> 启动前请务必更改.env中的apikey等必要设置。

配置完成后，将 .env.example 文件 **重命名为为 .env** 。

4. **启动游戏**：在 chemguess 目录下执行命令：

```bash
python run-server.py
```

并在浏览器中访问：[http://localhost:2300](http://localhost:2300)（若.env中设置了不同的端口，以具体设置为准）