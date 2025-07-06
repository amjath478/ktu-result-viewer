from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")  # Loads styled home page

@app.route("/result")
def result():
    try:
        output = subprocess.check_output( [r"venv\Scripts\python.exe", "opt2.py"], text=True, encoding="utf-8", errors="replace")
        return render_template("result.html", result=output)
    except Exception as e:
        return render_template("result.html", result=f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)

