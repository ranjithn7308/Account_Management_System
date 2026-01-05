from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

# ---------------- CONFIG ----------------
PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_FILE = os.path.join(BASE_DIR, 'accounts.txt')
STYLE_PATH = os.path.join(BASE_DIR, 'style.css')
# ----------------------------------------


# --------- DATA HANDLING ----------
def load_accounts():
    accounts = []
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                try:
                    acc_no, name, balance = line.strip().split(',')
                    accounts.append({
                        'number': acc_no,
                        'name': name,
                        'balance': balance
                    })
                except ValueError:
                    pass
    return accounts


def save_account(acc_no, name, balance):
    with open(ACCOUNTS_FILE, 'a') as f:
        f.write(f"{acc_no},{name},{balance}\n")
# ----------------------------------


class SimpleBankHandler(BaseHTTPRequestHandler):

    # ----------- GET REQUESTS -----------
    def do_GET(self):

        # HOME
        if self.path == '/' or self.path == '/home.html':
            self.serve_html('home.html')

        # STATIC HTML FILES
        elif self.path.endswith('.html'):
            self.serve_html(self.path.lstrip('/'))

        # CSS
        elif self.path == '/style.css':
            if os.path.exists(STYLE_PATH):
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open(STYLE_PATH, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'CSS file not found')

        # CHECK BALANCE
        elif self.path.startswith('/check_balance'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            acc_no = params.get('accountNumber', [''])[0]

            accounts = load_accounts()
            result = "<h2>No account number provided!</h2>"

            if acc_no:
                acc = next((a for a in accounts if a['number'] == acc_no), None)
                if acc:
                    result = f"""
                    <h2>Account Holder: {acc['name']}</h2>
                    <h3>Balance: {acc['balance']}</h3>
                    """
                else:
                    result = "<h2>Account not found!</h2>"

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Check Balance</title>
                <link rel="stylesheet" href="/style.css">
            </head>
            <body>
                <div class="container">
                    {result}
                    <a href="/check_balance.html">Back</a>
                </div>
            </body>
            </html>
            """

            self.respond_html(html)

        else:
            self.send_error(404, "Page not found")

    # ----------- POST REQUESTS -----------
    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode())

        # CREATE ACCOUNT
        if self.path == '/create':
            acc_no = data.get('accountNumber', [''])[0]
            name = data.get('accountName', [''])[0]
            balance = data.get('balance', [''])[0]

            accounts = load_accounts()
            exists = any(acc['number'] == acc_no for acc in accounts)

            if not acc_no or not name or not balance:
                msg = "All fields are required!"
            elif exists:
                msg = "Account already exists!"
            else:
                save_account(acc_no, name, balance)
                msg = "Account created successfully!"

            self.result_page(msg, '/create_account.html')

        # DEPOSIT
        elif self.path == '/deposit':
            self.handle_transaction(data, is_deposit=True)

        # WITHDRAW
        elif self.path == '/withdraw':
            self.handle_transaction(data, is_deposit=False)

        else:
            self.send_error(404, "Invalid request")

    # ----------- HELPERS -----------
    def serve_html(self, filename):
        file_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.respond_html(f.read())
        else:
            self.send_error(404, f"{filename} not found")

    def respond_html(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def result_page(self, msg, back_url):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Result</title>
            <link rel="stylesheet" href="/style.css">
        </head>
        <body>
            <div class="container">
                <h2>{msg}</h2>
                <a href="{back_url}">Back</a>
            </div>
        </body>
        </html>
        """
        self.respond_html(html)

    def handle_transaction(self, data, is_deposit=True):
        acc_no = data.get('accountNumber', [''])[0]
        amount = data.get('amount', [''])[0]

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except:
            self.result_page("Invalid amount!", "/home.html")
            return

        accounts = load_accounts()
        found = False

        for acc in accounts:
            if acc['number'] == acc_no:
                balance = float(acc['balance'])
                if not is_deposit and amount > balance:
                    self.result_page("Insufficient balance!", "/home.html")
                    return

                acc['balance'] = str(balance + amount if is_deposit else balance - amount)
                found = True
                break

        if found:
            with open(ACCOUNTS_FILE, 'w') as f:
                for acc in accounts:
                    f.write(f"{acc['number']},{acc['name']},{acc['balance']}\n")

            msg = "Deposit successful!" if is_deposit else "Withdrawal successful!"
        else:
            msg = "Account not found!"

        self.result_page(msg, "/home.html")


# ----------- SERVER START -----------
if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), SimpleBankHandler)
    print(f" Server running at http://localhost:{PORT}")
    server.serve_forever()
