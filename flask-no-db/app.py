from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB= {"notes":[]}

@app.get("/")
def index():
    return render_template("index.html", notes=DB["notes"])

@app.post("/add")
def add():
    text_to_save = request.form.get("text")
    if text_to_save:
        DB["notes"].append(text_to_save)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)