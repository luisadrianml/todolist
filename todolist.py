# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, g, request, url_for
import urllib
import json
import requests

HTTPString = "http://"
IP = "localhost:"
PORT = "6000"
ItemsApiDirection = "/api/"
items = "items"
addItems = "add"
delete = "delete/"
put="mark/"

fullAddress= HTTPString+IP+PORT+ItemsApiDirection

app = Flask(__name__)

@app.route("/")
def show_list():
    r = requests.get(fullAddress+items)
    r = r.json()
    return render_template('index.html', todolist=r)
    
@app.route("/add", methods=['POST'])
def add_entry():
    newTasks = {'what_to_do':request.form['what_to_do'],
             'due_date':request.form['due_date']}
    headers = {'content-type':'application/json'}
    r = requests.post(fullAddress+addItems,data=json.dumps(newTasks),headers=headers)
    return redirect(url_for('show_list'))

@app.route("/delete/<item>")
def delete_entry(item):
    item = urllib.parse.quote(item)
    requests.delete(fullAddress+delete+item)
    return redirect(url_for('show_list'))

@app.route("/mark/<item>")
def mark_as_done(item):
    item = urllib.parse.quote(item)
    requests.put(fullAddress+put+item)
    return redirect(url_for('show_list'))


if __name__ == "__main__":
    app.run("0.0.0.0",port=5000,debug=True)
