#!/bin/bash

echo "🚀 Starting Manager Bot..."
echo "Checking configuration..."

# Check if environment variables are set
if [ -z "$API_ID" ] || [ -z "$API_HASH" ] || [ -z "$BOT_TOKEN" ] || [ -z "$ADMIN_IDS" ]; then
    echo "❌ ERROR: Missing required environment variables!"
    echo "Please set: API_ID, API_HASH, BOT_TOKEN, ADMIN_IDS"
    exit 1
fi

echo "✅ Configuration OK"
echo "Starting bot..."

# Run the bot
python bot.py
