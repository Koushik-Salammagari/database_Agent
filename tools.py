from langchain.tools import tool
from db import get_connection

@tool
def execute_sql(query: str) -> str:
    """Executes raw SQL queries and returns results or confirmation."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
            return str(result)
        else:
            conn.commit()
            return "Query executed successfully."
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()
