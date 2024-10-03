from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import BOT_TOKEN, ADMIN_USER_ID, tasks
from utils.message_forwarder import forward_message
from utils.task_manager import manage_task

def start(update: Update, context: CallbackContext):
    """Display start message and available commands."""
    update.message.reply_text(
        "/create_task <task_name> - Create a new task\n"
        "/set_source <task_name> <channel_id> - Set source channel\n"
        "/set_target <task_name> <channel_id> - Set target channel\n"
        "/set_caption <task_name> <caption> - Set caption with hyperlink\n"
        "/start_task <task_name> - Start the task\n"
        "/stop_task <task_name> - Stop the task\n"
        "/status <task_name> - Check task status"
    )

def create_task(update: Update, context: CallbackContext):
    """Create a new task."""
    if len(context.args) < 1:
        update.message.reply_text("Please provide a task name.")
        return

    task_name = context.args[0]
    if task_name in tasks:
        update.message.reply_text("Task name already exists.")
        return
    
    tasks[task_name] = {"source": None, "target": None, "caption": None, "active": False}
    update.message.reply_text(f"Task '{task_name}' created successfully!")

def set_source(update: Update, context: CallbackContext):
    """Set source channel for a task."""
    manage_task(update, context, "source")

def set_target(update: Update, context: CallbackContext):
    """Set target channel for a task."""
    manage_task(update, context, "target")

def set_caption(update: Update, context: CallbackContext):
    """Set custom caption with hyperlink for a task."""
    manage_task(update, context, "caption")

def start_task(update: Update, context: CallbackContext):
    """Start the task to forward messages."""
    task_name = context.args[0]
    if tasks.get(task_name, {}).get("source") and tasks[task_name]["target"]:
        tasks[task_name]["active"] = True
        update.message.reply_text(f"Task '{task_name}' started successfully!")
    else:
        update.message.reply_text(f"Please set source and target for task '{task_name}'.")

def stop_task(update: Update, context: CallbackContext):
    """Stop an active task."""
    task_name = context.args[0]
    tasks[task_name]["active"] = False
    update.message.reply_text(f"Task '{task_name}' stopped.")

def forward_messages(update: Update, context: CallbackContext):
    """Forward messages from source to target channels if task is active."""
    for task_name, settings in tasks.items():
        if settings["active"]:
            forward_message(update, task_name, settings)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("create_task", create_task))
    dp.add_handler(CommandHandler("set_source", set_source, pass_args=True))
    dp.add_handler(CommandHandler("set_target", set_target, pass_args=True))
    dp.add_handler(CommandHandler("set_caption", set_caption, pass_args=True))
    dp.add_handler(CommandHandler("start_task", start_task, pass_args=True))
    dp.add_handler(CommandHandler("stop_task", stop_task, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, forward_messages))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
