import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot_manager import BotManager
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_IDS

# Initialize bot
app = Client(
    "manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize bot manager
bot_manager = BotManager()

# Admin check decorator
def admin_only(func):
    async def wrapper(client, message: Message):
        try:
            if message.from_user.id not in ADMIN_IDS:
                await message.reply_text("❌ You are not authorized to use this bot.")
                return
            return await func(client, message)
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")
    return wrapper

@app.on_message(filters.command("start"))
@admin_only
async def start_command(client, message: Message):
    try:
        welcome_text = """
🤖 **Bot Manager - Koyeb Multi-Bot Hosting**

Welcome! This bot allows you to run multiple Telegram bots from GitHub repositories.

**Available Commands:**
• /deploy - Deploy a new bot
• /list - Show all running bots
• /stop <bot_id> - Stop a bot
• /restart <bot_id> - Restart a bot
• /logs <bot_id> - View bot logs
• /status - System status

**How to deploy:**
1. Use /deploy command
2. Send bot token
3. Send GitHub repo URL
4. Send GitHub token (if private repo)
5. Wait for deployment

Let's get started! 🚀
"""
        await message.reply_text(welcome_text)
    except Exception as e:
        await message.reply_text(f"❌ Error in start command: {str(e)}")

@app.on_message(filters.command("deploy"))
@admin_only
async def deploy_command(client, message: Message):
    try:
        status_msg = await message.reply_text("🔄 Starting deployment process...\n\nPlease send the **Bot Token** for the bot you want to deploy.")
        
        # Store deployment state
        bot_manager.deployment_states[message.from_user.id] = {
            "step": "token",
            "status_msg_id": status_msg.id,
            "chat_id": message.chat.id
        }
    except Exception as e:
        await message.reply_text(f"❌ Error starting deployment: {str(e)}")

@app.on_message(filters.command("list"))
@admin_only
async def list_command(client, message: Message):
    try:
        bots = bot_manager.list_bots()
        
        if not bots:
            await message.reply_text("📭 No bots are currently running.")
            return
        
        text = "🤖 **Running Bots:**\n\n"
        for bot_id, info in bots.items():
            status = "🟢 Running" if info['status'] == 'running' else "🔴 Stopped"
            text += f"**Bot ID:** `{bot_id}`\n"
            text += f"**Status:** {status}\n"
            text += f"**Repo:** {info['repo_url']}\n"
            text += f"**Started:** {info['started_at']}\n"
            text += "─" * 30 + "\n\n"
        
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"❌ Error listing bots: {str(e)}")

@app.on_message(filters.command("stop"))
@admin_only
async def stop_command(client, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply_text("❌ Usage: /stop <bot_id>")
            return
        
        bot_id = args[1].strip()
        status_msg = await message.reply_text(f"🔄 Stopping bot `{bot_id}`...")
        
        success, msg = await bot_manager.stop_bot(bot_id)
        
        if success:
            await status_msg.edit_text(f"✅ {msg}")
        else:
            await status_msg.edit_text(f"❌ {msg}")
    except Exception as e:
        await message.reply_text(f"❌ Error stopping bot: {str(e)}")

@app.on_message(filters.command("restart"))
@admin_only
async def restart_command(client, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply_text("❌ Usage: /restart <bot_id>")
            return
        
        bot_id = args[1].strip()
        status_msg = await message.reply_text(f"🔄 Restarting bot `{bot_id}`...")
        
        success, msg = await bot_manager.restart_bot(bot_id)
        
        if success:
            await status_msg.edit_text(f"✅ {msg}")
        else:
            await status_msg.edit_text(f"❌ {msg}")
    except Exception as e:
        await message.reply_text(f"❌ Error restarting bot: {str(e)}")

@app.on_message(filters.command("logs"))
@admin_only
async def logs_command(client, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply_text("❌ Usage: /logs <bot_id>")
            return
        
        bot_id = args[1].strip()
        logs = bot_manager.get_logs(bot_id)
        
        if not logs:
            await message.reply_text(f"❌ No logs found for bot `{bot_id}`")
            return
        
        # Send logs as file if too long
        if len(logs) > 4000:
            with open(f"{bot_id}_logs.txt", "w") as f:
                f.write(logs)
            await message.reply_document(f"{bot_id}_logs.txt", caption=f"📄 Logs for bot `{bot_id}`")
            os.remove(f"{bot_id}_logs.txt")
        else:
            await message.reply_text(f"📄 **Logs for bot `{bot_id}`:**\n\n```\n{logs}\n```")
    except Exception as e:
        await message.reply_text(f"❌ Error fetching logs: {str(e)}")

@app.on_message(filters.command("status"))
@admin_only
async def status_command(client, message: Message):
    try:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        running_bots = len([b for b in bot_manager.bots.values() if b['status'] == 'running'])
        total_bots = len(bot_manager.bots)
        
        status_text = f"""
📊 **System Status**

🤖 **Bots:**
• Running: {running_bots}/{total_bots}

💻 **Resources:**
• CPU: {cpu_percent}%
• RAM: {memory.percent}% ({memory.used / (1024**3):.2f}GB / {memory.total / (1024**3):.2f}GB)
• Disk: {disk.percent}% ({disk.used / (1024**3):.2f}GB / {disk.total / (1024**3):.2f}GB)

✅ Manager Bot: Online
"""
        await message.reply_text(status_text)
    except Exception as e:
        await message.reply_text(f"❌ Error fetching status: {str(e)}")

@app.on_message(filters.text & filters.private)
@admin_only
async def handle_deployment_input(client, message: Message):
    try:
        user_id = message.from_user.id
        
        if user_id not in bot_manager.deployment_states:
            return
        
        state = bot_manager.deployment_states[user_id]
        step = state["step"]
        
        if step == "token":
            # Validate token format
            token = message.text.strip()
            if not token or ":" not in token:
                await message.reply_text("❌ Invalid token format. Please send a valid bot token.")
                return
            
            state["token"] = token
            state["step"] = "repo"
            await client.edit_message_text(
                state["chat_id"],
                state["status_msg_id"],
                "✅ Token received!\n\n🔄 Now send the **GitHub Repository URL** (e.g., https://github.com/user/repo)"
            )
        
        elif step == "repo":
            repo_url = message.text.strip()
            if not repo_url.startswith("http"):
                await message.reply_text("❌ Invalid GitHub URL. Please send a valid repository URL.")
                return
            
            state["repo_url"] = repo_url
            state["step"] = "github_token"
            await client.edit_message_text(
                state["chat_id"],
                state["status_msg_id"],
                "✅ Repository URL received!\n\n🔄 If this is a **private repository**, send your GitHub Personal Access Token.\n\nIf it's public, send: `skip`"
            )
        
        elif step == "github_token":
            github_token = message.text.strip()
            if github_token.lower() != "skip":
                state["github_token"] = github_token
            else:
                state["github_token"] = None
            
            # Start deployment
            await client.edit_message_text(
                state["chat_id"],
                state["status_msg_id"],
                "🚀 Starting deployment...\n\nThis may take a few minutes. Please wait..."
            )
            
            # Deploy bot
            success, msg, bot_id = await bot_manager.deploy_bot(
                state["token"],
                state["repo_url"],
                state["github_token"]
            )
            
            if success:
                await client.edit_message_text(
                    state["chat_id"],
                    state["status_msg_id"],
                    f"✅ **Deployment Successful!**\n\n**Bot ID:** `{bot_id}`\n**Status:** Running\n**Repository:** {state['repo_url']}\n\nYou can manage this bot using:\n• /stop {bot_id}\n• /restart {bot_id}\n• /logs {bot_id}"
                )
            else:
                await client.edit_message_text(
                    state["chat_id"],
                    state["status_msg_id"],
                    f"❌ **Deployment Failed!**\n\n**Error:** {msg}\n\nPlease check the error and try again with /deploy"
                )
            
            # Clear deployment state
            del bot_manager.deployment_states[user_id]
    
    except Exception as e:
        await message.reply_text(f"❌ Error processing input: {str(e)}")
        if message.from_user.id in bot_manager.deployment_states:
            del bot_manager.deployment_states[message.from_user.id]

# Run the bot
if __name__ == "__main__":
    try:
        print("🤖 Manager Bot starting...")
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
