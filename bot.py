from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

# Replace with your own details
api_id = '25236906'
api_hash = '2c7b117fb4fb4d487df4e589da1d4c5f'
bot_token = '7995816359:AAESeFlM6x7wiFh5Lhv_iua8v7-hOs1ihqc'

# File to store tasks
TASKS_FILE = 'tasks.json'

# Create a new Pyrogram client
app = Client('junction_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

# Initialize tasks
tasks = load_tasks()

# Add new task command
@app.on_message(filters.command('add_task') & filters.private)
async def add_task(client, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            await message.reply("Usage: /add_task source_channel_id target_channel_id")
            return

        source_channel = parts[1]
        target_channel = parts[2]

        # Add the task
        tasks[source_channel] = target_channel
        save_tasks(tasks)
        await message.reply(f"Task added: {source_channel} -> {target_channel}")
    except Exception as e:
        await message.reply(f"Error adding task: {e}")

# List all active tasks command
@app.on_message(filters.command('list_tasks') & filters.private)
async def list_tasks(client, message: Message):
    if not tasks:
        await message.reply("No active tasks.")
        return

    task_list = "\n".join([f"{src} -> {dst}" for src, dst in tasks.items()])
    await message.reply(f"Active tasks:\n{task_list}")

# Delete task command
@app.on_message(filters.command('delete_task') & filters.private)
async def delete_task(client, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Usage: /delete_task source_channel_id")
            return

        source_channel = parts[1]

        if source_channel in tasks:
            del tasks[source_channel]
            save_tasks(tasks)
            await message.reply(f"Task for {source_channel} deleted.")
        else:
            await message.reply(f"No task found for {source_channel}.")
    except Exception as e:
        await message.reply(f"Error deleting task: {e}")

# Monitor channels for new files and forward them
@app.on_message(filters.document | filters.video | filters.photo)
async def forward_files(client, message: Message):
    source_channel = str(message.chat.id)
    if source_channel in tasks:
        target_channel = tasks[source_channel]
        try:
            await message.copy(chat_id=target_channel)
            print(f"File from {source_channel} copied to {target_channel}.")
        except Exception as e:
            print(f"Error copying file: {e}")

if __name__ == '__main__':
    print("Bot is running...")
    app.run()
