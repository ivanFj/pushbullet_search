from flask import Flask, render_template, request, render_template_string, redirect, url_for
import html, requests, codecs, signup, get_pushes, delete_update_pushes

app = Flask(__name__)
MAPSAPIKEY = "AIzaSyDSV6NLPT0W75HsDPIlsE3yu3YyGhIQSgw"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html")

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/rot13', methods = ['GET', 'POST'])
def rot13():
    if request.method == "GET":
        return render_template("rot13.html", text = "")
    else:
        return render_template("rot13.html", text = html.escape(codecs.encode(request.form["text"], 'rot13')) )

@app.route("/pokeball")
def pokeball():
    return render_template("pokeball.html")

@app.route("/sign_up", methods = ["GET", "POST"])
def account_signup():
    if request.method == "GET":
        return render_template("sign_up.html")
    else:
        attempt = signup.validate_signup(username = request.form['username'], password = request.form['password'], verify = request.form['verify'], email = request.form['email'])
        if attempt[0]:
            return redirect(url_for("account_success", username = attempt[1]))
        else:
            return render_template("sign_up.html", **attempt[1])

@app.route("/welcome")
def account_success():
    return render_template("welcome.html", username =  request.args.get('username'))

@app.route("/searchbullet", methods = ["GET", "POST"])
def searchbullet():
    if request.method == "GET":
        return render_template("searchbullet.html", pushes = "", hide = 'hide')
    else:
        ##Access Token = o.ARtmiAG3zSUx5UNtkUAM6XS8BciFTfwy
        token =  {"Access-Token" : request.form.get("token")}
        pushes = get_pushes.get_pushes(token)
        return render_template("searchbullet.html", pushes = pushes, hide = '')

@app.route("/updatepushes")
def updatepushes():
    inserts = delete_update_pushes.get()
    return render_template("updatepushes.html", **inserts)

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)