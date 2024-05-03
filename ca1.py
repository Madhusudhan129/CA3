from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
    <head><title>Vulnerable Website</title></head>
    <body>
    <h1>Welcome to the Vulnerable Website!</h1>
    <p>This website is intentionally vulnerable to demonstrate Local File Inclusion (LFI) vulnerabilities.</p>
    <p>To test for LFI vulnerability, try accessing the following URL:</p>
    <p>http://localhost:5000/vulnerable?file=/etc/passwd</p>
    </body>
    </html>
    """

@app.route('/vulnerable')
def vulnerable():
    file_path = request.args.get('file', '')

    # List of sensitive files and directories
    sensitive_files = [
        "/etc/passwd",
        "/etc/hosts",
        "/etc/shadow",
        "/etc/group",
        "/etc/issue",
        "/etc/hostname",
        "/proc/self/environ",
        "/proc/version",
        "/proc/cmdline",
        "/proc/mounts",
        "/etc/httpd/conf/httpd.conf",
        "/etc/nginx/nginx.conf",
        "/etc/apache2/apache2.conf",
        "/etc/php/php.ini",
        "/var/log/apache2/access.log",
        "/var/log/apache2/error.log",
        "/var/log/nginx/access.log",
        "/var/log/nginx/error.log",
        "/var/log/httpd/access.log",
        "/var/log/httpd/error.log"
    ]

    # Check if the requested file is in the list of sensitive files
    if file_path in sensitive_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Error: Access to this file is not allowed."

if __name__ == '__main__':
    app.run(debug=True)

