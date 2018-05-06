# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 22:54:40 2018

@author: LuisMartinez
"""
#!flask/bin/python
from flask import Flask, jsonify, request, abort, redirect, g, url_for
from firebase import firebase

app = Flask(__name__)
app.config.from_object(__name__)
firebase = firebase.FirebaseApplication('https://fir-project-d6004.firebaseio.com/', None)


@app.route('/api/items',methods=['GET'])
def get_items():
    result = firebase.get('/items', None)
    if result!=None:
        tdlist = [dict(what_to_do=key, due_date=value.get("due_date"), status=value.get("status"))
                  for key,value in result.items()]
    else:
        tdlist = {}
    return jsonify(tdlist)

@app.route('/api/add', methods=['POST'])
def insert_task():
    result = firebase.patch('/items/'+request.json.get("what_to_do"), dict(due_date=request.json.get("due_date"), status=""))
    print(result!=None)
    return jsonify({'result': result_message(result)})

@app.route('/api/mark/<string:item>', methods=['PUT'])
def update_task(item):    
    result = firebase.patch('/items/'+item, dict(status="done"))    
    print(result!=None)
    return jsonify({'result': result_message(result)})

@app.route('/api/delete/<string:item>', methods=['DELETE'])
def delete_task(item):       
    result = firebase.delete('/items', item)
    print(result)
    return jsonify({'result': result_message(result)})

def result_message(result):
    if result==None:
        return False
    else:
        return True

if __name__ == '__main__':
    app.run("0.0.0.0",port=6000,debug=True)