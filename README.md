# Telegram Junction Bot

This bot forwards new messages from a source channel to a target channel with admin permission in both channels. It supports multiple tasks, each with its own settings for source, target, custom captions, and hyperlinks.

## Setup

1. Clone the repository.
2. Install the dependencies: `pip install -r requirements.txt`.
3. Set up the `.env` file with your bot token and admin user ID.
4. Run the bot: `python bot.py`.

## Commands

- `/start` - Show available commands.
- `/create_task <task_name>` - Create a new task.
- `/set_source <task_name> <channel_id>` - Set source channel.
- `/set_target <task_name> <channel_id>` - Set target channel.
- `/set_caption <task_name> <caption>` - Set caption with hyperlink.
- `/start_task <task_name>` - Start forwarding messages for the task.
- `/stop_task <task_name>` - Stop forwarding messages for the task.
- `/status <task_name>` - Check the status of a task.
