import sqlite3

# Improved user login function with parameterized queries and better error handling.
def user_login(username, password):
    # Establish a database connection
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Use parameterized queries to prevent SQL injection
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            return True  # Login successful
        else:
            return False  # Login failed

    except sqlite3.Error as e:
        print(f'An error occurred: {e}')  # Better error handling
        return False
    finally:
        if conn:
            conn.close()  # Ensure the connection is closed properly

# Example usage
if __name__ == '__main__':
    username = 'test_user'
    password = 'secure_password'
    if user_login(username, password):
        print('Login successful!')
    else:
        print('Login failed!')