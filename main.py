import sqlite3
import http.server
import socketserver
import threading

DATABASE = "sql.db"

def main():
    create_server()
    create_sql()
    user = get_user()
    app_name = 'SQL SERVER'
    print(f"Welcome, {user}!")
    cmd = input(f"{user}@{app_name}--> ")
    while cmd != "exit":
        if cmd == "help":
            help()
        elif cmd == "html":
            start_html_server()
        elif cmd == "add_user":
            add_user()
        elif cmd == "view_users":
            view_users()
        else:
            print("Invalid command. Type 'help' for options.")
        cmd = input(f"{user}@{app_name}--> ")
    print("Exiting the application.")

def create_server():
    server_name = 'SQL SERVER'
    print(f"Server '{server_name}' created successfully.")

def get_user():
    return input("Enter your username: ")

def create_sql():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("SQL database initialized.")

def add_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender (M/F): ")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, age, gender) VALUES (?, ?, ?, ?)", 
                   (username, password, age, gender))
    conn.commit()
    conn.close()
    print("User added successfully.")

def view_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, age, gender FROM users")
    users = cursor.fetchall()
    conn.close()
    if users:
        print("Users in the database:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Age: {user[2]}, Gender: {user[3]}")
    else:
        print("No users found in the database.")

def generate_html():
    """Generate HTML content for database records."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, age, gender FROM users")
    users = cursor.fetchall()
    conn.close()

    html_content = """
    <html>
        <head><title>User Data</title></head>
        <body>
            <h1>User Data</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Age</th>
                    <th>Gender</th>
                </tr>
    """
    for user in users:
        html_content += f"""
                <tr>
                    <td>{user[0]}</td>
                    <td>{user[1]}</td>
                    <td>{user[2]}</td>
                    <td>{user[3]}</td>
                </tr>
        """
    html_content += """
            </table>
        </body>
    </html>
    """
    return html_content

def start_html_server():
    """Start an HTTP server to display user data as HTML."""
    PORT = 8000

    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html_content = generate_html()
                self.wfile.write(html_content.encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()

    def run_server():
        with socketserver.TCPServer(("127.0.0.1", PORT), RequestHandler) as httpd:
            print(f"Serving at http://localhost:{PORT}")
            print(f"Access via your local IP: http://<your-local-ip>:{PORT}")
            httpd.serve_forever()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

def help():
    print("This app helps manage SQL by using user data on a local server.")
    print("Commands:")
    print("  help        - Show this help message")
    print("  html        - Start an HTTP server to display user data")
    print("  add_user    - Add a new user to the database")
    print("  view_users  - View all users in the database")
    print("  exit        - Exit the application")

if __name__ == "__main__":
    main()