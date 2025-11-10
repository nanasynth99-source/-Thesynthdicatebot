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
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'your_channel_username')
PORT = int(os.getenv('PORT', 8443))

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message with a button to join the channel when the command /start is issued."""
    
    # Create inline keyboard with join button
    keyboard = [
        [InlineKeyboardButton("Join Our Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
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
            # Get user chat member status in the channel
            chat_member = await context.bot.get_chat_member(
                chat_id=f"@{CHANNEL_USERNAME}", 
                user_id=query.from_user.id
            )
            
            # Check if user is a member (member, administrator, creator)
            if chat_member.status in ['member', 'administrator', 'creator']:
                await query.edit_message_text(
                    "🎉 Thank you for joining our channel! You now have access to the bot.\n\n"
                    "Feel free to explore our features!"
                )
            else:
                await query.edit_message_text(
                    "❌ It seems you haven't joined our channel yet. Please join using the button below and try again.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Join Our Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
                        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
                    ])
                )
                
        except Exception as e:
            logger.error(f"Error checking channel membership: {e}")
            await query.edit_message_text(
                "❌ There was an error verifying your membership. Please try again later."
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
