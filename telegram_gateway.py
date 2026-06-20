import os
import sqlite3
import telebot

# Retrieve the Telegram Token from environment variables for security
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("System Failure: TELEGRAM_BOT_TOKEN environment variable is not set!")

bot = telebot.TeleBot(TOKEN)

DB_DIR = os.path.join(os.getcwd(), ".neev")
DB_PATH = os.path.join(DB_DIR, "memory.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🤖 **Neev AI IDE - Mobile Gateway Activated**\n\n"
        "Use this interface to query and update your persistent memory engram layer directly from your device.\n\n"
        "**Commands:**\n"
        "📝 `/save topic | content` - Store a new architectural rule or context.\n"
        "🔍 `/view topic` - Retrieve saved memories (use `/view all` for everything).\n"
        "❌ `/delete id` - Scrub a corrupted memory by its ID number."
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['save'])
def save_engram(message):
    try:
        raw_args = message.text.split('/save ', 1)[1]
        if '|' not in raw_args:
            bot.reply_to(message, "❌ Format Error. Use: `/save topic | your content here`", parse_mode="Markdown")
            return
        
        topic, content = raw_args.split('|', 1)
        topic = topic.strip()
        content = content.strip()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO memories (topic, content) VALUES (?, ?)', (topic, content))
            conn.commit()

        bot.reply_to(message, f"✅ **Memory Embedded Successfully!**\nTopic: `{topic}`", parse_mode="Markdown")
    except IndexError:
        bot.reply_to(message, "❌ Please provide a topic and content. Example: `/save ui_rules | Use dark mode layout`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ System Failure: {str(e)}")

@bot.message_handler(commands=['view'])
def view_engram(message):
    try:
        topic = message.text.split('/view ', 1)[1].strip()
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if topic.lower() == 'all':
                cursor.execute('SELECT id, topic, content, timestamp FROM memories ORDER BY timestamp DESC LIMIT 20')
            else:
                cursor.execute('SELECT id, topic, content, timestamp FROM memories WHERE topic = ? ORDER BY timestamp DESC', (topic,))
            
            results = cursor.fetchall()

        if not results:
            bot.reply_to(message, f"ℹ️ No memories found under the topic: `{topic}`", parse_mode="Markdown")
            return

        response_lines = ["🔍 **Retrieved Memories:**\n"]
        for row in results:
            response_lines.append(f"🆔 **ID:** `{row[0]}` | 📂 **Topic:** `{row[1]}`\n📝 {row[2]}\n📅 _{row[3]}_\n---")
        
        full_response = "\n".join(response_lines)
        if len(full_response) > 4000:
            full_response = full_response[:3900] + "\n...[Truncated]..."
            
        bot.reply_to(message, full_response, parse_mode="Markdown")
    except IndexError:
        bot.reply_to(message, "❌ Please specify a topic. Example: `/view ui_rules` or `/view all`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ System Failure: {str(e)}")

@bot.message_handler(commands=['delete'])
def delete_engram(message):
    try:
        memory_id = int(message.text.split('/delete ', 1)[1].strip())
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
            conn.commit()
            changes = cursor.rowcount

        if changes > 0:
            bot.reply_to(message, f"🔥 **Memory ID {memory_id} successfully scrubbed.**", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ Memory ID `{memory_id}` was not found.", parse_mode="Markdown")
    except (IndexError, ValueError):
        bot.reply_to(message, "❌ Please specify a valid numeric ID. Example: `/delete 5`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ System Failure: {str(e)}")

if __name__ == "__main__":
    print("Neev Mobile Telegram Gateway is running...")
    bot.infinity_polling()
  
