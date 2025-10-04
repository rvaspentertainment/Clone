# 🚀 Koyeb Deployment - Step by Step Guide

## ⚠️ Fix for "no command to run" Error

The error you're seeing is because Koyeb doesn't know how to start your application. Here's how to fix it:

## 📋 Solution 1: Using Procfile (Recommended)

The repository already includes a `Procfile` with:
```
web: python bot.py
```

Make sure this file exists in your GitHub repo root.

## 📋 Solution 2: Set Run Command in Koyeb

When deploying on Koyeb:

1. Go to **Advanced** settings
2. Find **Run Command** field
3. Enter: `python bot.py`
4. Save and deploy

## 🔧 Complete Deployment Steps

### 1. Prepare Your Repository

Ensure your repo has these files:
```
├── bot.py
├── bot_manager.py
├── config.py
├── storage.py
├── Dockerfile
├── Procfile          ← Important!
├── requirements.txt
├── start.sh
└── .gitignore
```

### 2. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 3. Deploy on Koyeb

**Step 1: Create New App**
- Go to https://app.koyeb.com
- Click **"Create App"**

**Step 2: Select Source**
- Choose **"GitHub"**
- Connect your GitHub account
- Select your repository
- Branch: `main` (or your default branch)

**Step 3: Configure Build**
- **Builder**: Dockerfile
- **Dockerfile**: `Dockerfile` (auto-detected)

**Step 4: Set Environment Variables**

Click **"Add Variable"** for each:

| Variable | Value | Example |
|----------|-------|---------|
| `API_ID` | Your Telegram API ID | `12345678` |
| `API_HASH` | Your Telegram API Hash | `abc123def456` |
| `BOT_TOKEN` | Your Manager Bot Token | `123456:ABC-DEF` |
| `ADMIN_IDS` | Your Telegram User ID | `987654321` |

**Step 5: Advanced Settings**
- **Instance**: Nano (Free)
- **Region**: Choose closest
- **Port**: 8000 (or leave default)
- **Run Command**: `python bot.py` OR leave empty (Procfile handles it)
- **Health Checks**: Disabled

**Step 6: Deploy**
- Click **"Deploy"**
- Wait 3-5 minutes for build and deployment

### 4. Verify Deployment

**Check Logs:**
1. Go to Koyeb Dashboard
2. Click your service
3. Go to **"Logs"** tab
4. Look for: `🤖 Manager Bot starting...`

**Expected Output:**
```
✅ Configuration validated successfully
🤖 Manager Bot starting...
INFO:pyrogram.session.session:Session started
INFO:bot_manager:Base directory created/verified: /app/deployed_bots
```

**Test Bot:**
1. Open Telegram
2. Find your Manager Bot
3. Send `/start`
4. You should get a welcome message!

## 🐛 Troubleshooting

### Error: "Application exited with code 1"

**Cause:** Configuration error or missing environment variables

**Fix:**
1. Check all 4 environment variables are set in Koyeb
2. Verify tokens are correct (no extra spaces)
3. Check Koyeb logs for specific error
4. Redeploy the service

### Error: "no command to run"

**Cause:** Missing Procfile or run command

**Fix Option 1:**
- Add `Procfile` to repo with: `web: python bot.py`
- Push to GitHub
- Redeploy on Koyeb

**Fix Option 2:**
- In Koyeb, go to Service Settings
- Set **Run Command**: `python bot.py`
- Redeploy

### Error: "failed to solve with frontend dockerfile"

**Cause:** Dockerfile syntax error

**Fix:**
- Ensure Dockerfile exists
- Check Dockerfile syntax
- Try deploying again

### Bot doesn't respond on Telegram

**Check:**
1. Is bot running? Check Koyeb logs
2. Is BOT_TOKEN correct?
3. Did you talk to the right bot? Check @BotFather
4. Is your USER_ID in ADMIN_IDS?

## 📊 Monitoring

### Check Bot Status

**Via Koyeb Dashboard:**
- Go to your service
- Check "Status" → should be "Running"
- Check "Logs" for errors

**Via Telegram:**
- Send `/status` to your bot
- Should show system resources

### View Logs

**Koyeb Logs:**
```
Dashboard → Your Service → Logs Tab
```

**Bot Logs:**
Send `/logs <bot_id>` to view deployed bot logs

## 🔄 Updating Your Bot

### Method 1: Auto-deploy (Recommended)

1. Make changes to your code
2. Push to GitHub: `git push`
3. Koyeb auto-redeploys (if enabled)

### Method 2: Manual Redeploy

1. Go to Koyeb Dashboard
2. Click your service
3. Click **"Redeploy"**

## 💡 Tips

1. **Free Tier Limits:**
   - 1 service only
   - 512MB RAM
   - Ephemeral storage
   - Deploy wisely!

2. **Bot Persistence:**
   - Deployed bots auto-restore on restart
   - Full instance recreation = need to redeploy bots

3. **Resource Management:**
   - Check `/status` regularly
   - Don't deploy too many heavy bots
   - Stop unused bots with `/stop`

4. **Security:**
   - Never commit tokens to GitHub
   - Use Koyeb environment variables
   - Keep tokens secure

## ✅ Success Checklist

- [ ] All files in repository
- [ ] Procfile exists
- [ ] Pushed to GitHub
- [ ] Environment variables set in Koyeb
- [ ] Deployment successful
- [ ] Bot responds to `/start`
- [ ] Can deploy test bot with `/deploy`

## 🎯 Next Steps

Once deployed successfully:

1. **Deploy your first bot:**
   - Send `/deploy` to Manager Bot
   - Follow the prompts
   - Provide bot token, repo URL, GitHub token

2. **Manage bots:**
   - Use `/list` to see all bots
   - Use `/logs <bot_id>` to check logs
   - Use `/stop <bot_id>` to stop bots

3. **Monitor system:**
   - Use `/status` to check resources
   - Keep eye on RAM usage

## 🆘 Still Having Issues?

1. **Double-check environment variables**
2. **Review Koyeb logs carefully**
3. **Ensure Procfile exists**
4. **Try manual run command: `python bot.py`**
5. **Check if bot token is valid**
6. **Verify API_ID and API_HASH are correct**

---

**Happy Deploying! 🚀**

If you follow this guide, your bot will be running on Koyeb successfully!
