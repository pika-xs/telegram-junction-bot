from telegram import ParseMode

def forward_message(update, task_name, settings):
    source_channel = settings["source"]
    target_channel = settings["target"]
    caption = settings["caption"]
    
    if update.message.chat_id == source_channel:
        forward_text = update.message.text
        if caption:
            caption_text = f"{caption} — [Source]({update.message.link})"
        else:
            caption_text = None

        update.message.bot.send_message(
            chat_id=target_channel,
            text=forward_text,
            caption=caption_text,
            parse_mode=ParseMode.MARKDOWN
        )
