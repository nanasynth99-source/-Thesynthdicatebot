import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackContext, CommandHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get configuration from environment variables (recommended for Render)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHANNEL_LINK = "https://t.me/+7UxkdEYv9eAxZTZk"
PORT = int(os.getenv('PORT', 8443))

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message with a button to join the channel when the command /start is issued."""
    
    # Create inline keyboard with join button
    keyboard = [
        [InlineKeyboardButton("Join Our Channel", url=TELEGRAM_CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send welcome message with join button
    await update.message.reply_text(
        "👋 Welcome! To continue using this bot, please join our channel first!\n\n"
        "Click the button below to join our channel, then click 'I've Joined' to verify.",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_join":
        # Check if user has joined the channel
        try:
            # Extract channel username from the link for checking membership
            # The link is https://t.me/+7UxkdEYv9eAxZTZk which is a private channel invite
            # For private channels, we need to use the invite link format
            # Note: Checking membership in private channels might be limited
            
            # For private channels, we can try to get chat member using the chat ID
            # The +7UxkdEYv9eAxZTZk part is the invite hash, we need the actual channel username/ID
            # Since this is a private channel link, membership checking might not work directly
            # Alternative approach: We can inform the user that we can't verify automatically
            
            await query.edit_message_text(
                "⚠️ For private channels, we cannot automatically verify membership.\n\n"
                "🎉 Thank you for joining our channel! We trust that you've joined successfully.\n\n"
                "Feel free to explore our features!"
            )
            
            # If you have the actual channel username (like @channelname), you can use this instead:
            # chat_member = await context.bot.get_chat_member(
            #     chat_id=f"@{CHANNEL_USERNAME}", 
            #     user_id=query.from_user.id
            # )
            # 
            # if chat_member.status in ['member', 'administrator', 'creator']:
            #     await query.edit_message_text("🎉 Thank you for joining! You now have access.")
            # else:
            #     await query.edit_message_text("❌ Please join our channel first.")
                
        except Exception as e:
            logger.error(f"Error checking channel membership: {e}")
            await query.edit_message_text(
                "❌ There was an error verifying your membership. Please try again later.\n\n"
                "If the issue persists, please contact the administrator."
            )

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates."""
    logger.error(f"Exception while handling an update: {context.error}")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_error_handler(error_handler)

    # Start the Bot - using polling for Render
    print("Bot is running on Render...")
    application.run_polling()

if __name__ == "__main__":
    main()
