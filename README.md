🐚 Py-Smart-Shell

A Python-powered smart terminal that mimics the behavior of a real shell.
It supports standard commands, system monitoring, and even natural language AI mode so that anyone (even non-technical users) can run commands like:

$ show me the current directory
$ create a folder test
$ what's the cpu usage

✨ Features

🔹 File & Directory Operations: pwd, ls, cd, mkdir, rm, cat, echo

🔹 System Monitoring: cpu, mem, ps

🔹 System Info: whoami, date, uptime, history, clear

🔹 Natural Language AI Mode:

Example: create a folder called test and open it → mkdir test && cd test

🔹 Web-based Interface with real-time typing animation

🔹 Error handling for invalid commands

🔹 Clean, shell-like prompt with username & hostname

🚀 Getting Started
1. Clone the repository
git clone https://github.com/rajatbaranwal/py-smart-shell.git
cd py-smart-shell

2. Install dependencies
pip install -r requirements.txt

3. Run the app
python app.py

4. Open in browser

Go to: http://127.0.0.1:5000/

📂 Project Structure
py-smart-shell/
│── app.py              # Flask web server
│── main.py             # CLI version of terminal
│── commands.py         # File system operations
│── monitor.py          # CPU, memory, process monitoring
│── nlp_parser.py       # Natural language → command parser
│── templates/
│   └── index.html      # Frontend terminal UI
│── static/
│   └── style.css       # Styling for terminal
│── requirements.txt    # Dependencies

🌐 Deployment

Deployed using Render.
For deployment:

Push to GitHub

Connect Render → Web Service → Python → set Start Command as:

gunicorn app:app


Access your web terminal online 🎉

🧠 Future Enhancements

🔮 More natural language support (move, copy, rename files)

⌨️ Auto-completion for commands

📝 Command history persistence

🌍 Multi-user support

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
