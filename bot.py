import os
import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ---------------- CONFIGURATION ----------------

BOT_TOKEN = os.environ["BOT_TOKEN"]

CHANNEL_ID = "@getjobbrotherjobs"

CHANNEL_LINK = "https://t.me/getjobbrotherjobs"

PDF_LINK = "https://drive.google.com/file/d/1VPwlbm7LXdV_MaGTsKuaqxGNFyoVGsy5/view?usp=sharing"

# ---------------- LOGGING ----------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ---------------- START COMMAND ----------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        [
            InlineKeyboardButton(
                "JOIN TELEGRAM CHANNEL",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "I HAVE JOINED",
                callback_data="verify"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to GET JOB BROTHER!\n\n"
        "Please join our Telegram channel "
        "to access PDF materials.\n\n"
        "After joining, click I HAVE JOINED.",
        reply_markup=reply_markup
    )


# ---------------- VERIFY MEMBERSHIP ----------------

async def verify(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    # Stop Telegram loading indicator
    await query.answer("Checking membership...")

    user_id = query.from_user.id

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "DOWNLOAD PDF",
                        url=PDF_LINK
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                "Congratulations!\n\n"
                "Your channel membership is verified.\n\n"
                "Your PDF material is ready"
                "pdf only read access if you want pdf dm"      ,
                reply_markup=reply_markup
            )

        else:

            await query.answer(
                "Please join our Telegram channel first!",
                show_alert=True
            )

    except Exception as error:

        logger.exception(
            "Membership verification failed"
        )

        await query.message.reply_text(
            "Unable to verify your membership.\n"
            "Please try again later."
        )


# ---------------- MAIN APPLICATION ----------------

def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            verify,
            pattern="^verify$"
        )
    )

    print("GET JOB BROTHER BOT STARTED SUCCESSFULLY!")

    app.run_polling()


if __name__ == "__main__":
    main()
