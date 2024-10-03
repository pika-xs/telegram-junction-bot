from config import tasks

def manage_task(update, context, key):
    """Helper function to manage task settings."""
    if len(context.args) < 2:
        update.message.reply_text(f"Please provide a task name and {key}.")
        return

    task_name = context.args[0]
    if task_name not in tasks:
        update.message.reply_text(f"Task '{task_name}' does not exist.")
        return

    value = context.args[1]
    tasks[task_name][key] = value
    update.message.reply_text(f"Task '{task_name}' {key} set to {value}.")
