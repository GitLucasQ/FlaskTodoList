from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb
import datetime

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/users', methods=['GET'])
def GetUsers():
    db = MySQLdb.connect('localhost', 'root', '', 'todo')
    cursor = db.cursor()
    cursor.execute('select * from users')
    result = jsonify(cursor.fetchall())
    db.close()

    return result


@app.route('/api/newUser', methods=['POST'])
def NewUser():
    db = MySQLdb.connect('localhost', 'root', '', 'todo')
    json = request.get_json()
    username = json['username']
    cursor = db.cursor()
    query = "insert into users (username, createdAt) values (%s, %s)"
    try:
        cursor.execute(query, (username, datetime.datetime.now()))
        db.commit()
        db.close()
        return 'Insert succesfully'
    except Exception as e:
        return str(e)

@app.route('/api/deleteUser/<id>', methods=['DELETE'])
def DeleteUser(id):
    db = MySQLdb.connect('localhost', 'root', '', 'todo')        
    cursor = db.cursor()
    query = "delete from users where id = %s"    
    try:
        cursor.execute(query, (id))
        db.commit()
        db.close()
        return 'Delete succesfully'
    except Exception as e:
        return str(e)

@app.route('/api/newNote', methods=['POST'])
def NewNote():
    db = MySQLdb.connect('localhost', 'root', '', 'todo')        
    json = request.get_json()
    data = (json['user'], json['title'], json['description'], json['date'],)
    cursor = db.cursor()
    query = "insert into notes (user, title, description, dateNote) values (%s, %s, %s, %s)"
    try:
        cursor.execute(query, data)
        db.commit()
        db.close()
        return 'Note inserted succesfully'
    except Exception as e:
        return str(e)


@app.route('/api/notes', methods=['GET'])
def GetNotes():
    db = MySQLdb.connect('localhost', 'root', '', 'todo')
    cursor = db.cursor()
    cursor.execute('select * from notes')
    result = jsonify(cursor.fetchall())
    db.close()
    return result


@app.route('/api/getnote/<id>', methods=['GET'])
def GetNoteDescription(id):
    db = MySQLdb.connect('localhost', 'root', '', 'todo')
    cursor = db.cursor()
    cursor.execute('select * from notes where id = %s', id)
    result = jsonify(cursor.fetchall())
    db.close()
    return result


@app.route('/api/deleteNote/<id>', methods=['DELETE'])
def DeleteNote(id):
    db = MySQLdb.connect('localhost', 'root', '', 'todo')        
    cursor = db.cursor()
    query = "delete from notes where id = %s"    
    try:
        cursor.execute(query, (id))
        db.commit()
        db.close()
        return 'Delete succesfully'
    except Exception as e:
        return str(e)


@app.route('/api/updateNote/<id>', methods=['PUT'])
def UpdateNote(id):
    db = MySQLdb.connect('localhost', 'root', '', 'todo')  
    json = request.get_json()   
    data = (json['user'], json['title'], json['description'], json['date'],)   
    cursor = db.cursor()
    query = "update notes set user = %s, title = %s, description = %s, dateNote = %s where id = " + id    
    try:
        cursor.execute(query, (data))
        db.commit()
        db.close()
        return 'Update succesfully'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
