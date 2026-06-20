import sqlite3
import os
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server for the Shadow Code ecosystem
mcp = FastMCP("Neev Memory Server")

# Define the local database path strictly inside the project directory
DB_DIR = os.path.join(os.getcwd(), ".neev")
DB_PATH = os.path.join(DB_DIR, "memory.db")

def init_db():
    """Initialize the local SQLite database with the foundational engram table."""
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Ensure the database structure is ready before the server starts
init_db()

@mcp.tool()
def save_memory(topic: str, content: str) -> str:
    """
    Save a new context, architectural rule, or preference to the local database.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO memories (topic, content) VALUES (?, ?)', 
                (topic, content)
            )
            conn.commit()
        return f"Successfully embedded memory under topic: '{topic}'"
    except Exception as e:
        return f"System Failure - Could not save memory: {str(e)}"

@mcp.tool()
def retrieve_memory(topic: str) -> str:
    """
    Retrieve all saved contextual memories related to a specific topic.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            if topic.lower() == 'all':
                cursor.execute('SELECT id, topic, content, timestamp FROM memories ORDER BY timestamp DESC LIMIT 50')
            else:
                cursor.execute(
                    'SELECT id, topic, content, timestamp FROM memories WHERE topic = ? ORDER BY timestamp DESC', 
                    (topic,)
                )
                
            results = cursor.fetchall()
            
            if not results:
                return f"No memories found for topic: '{topic}'"
                
            formatted_results = []
            for row in results:
                formatted_results.append(f"[ID: {row[0]}] ({row[3]}) {row[1]}: {row[2]}")
                
            return "\n".join(formatted_results)
    except Exception as e:
        return f"System Failure - Could not retrieve memory: {str(e)}"

@mcp.tool()
def delete_memory(memory_id: int) -> str:
    """
    Delete a specific memory by its ID to prevent memory poisoning.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return f"Successfully scrubbed memory ID: {memory_id} from the engram."
            else:
                return f"Memory ID {memory_id} does not exist."
    except Exception as e:
        return f"System Failure - Could not delete memory: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
