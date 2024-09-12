from flask import Flask,render_template,request,redirect
import sqlite3
from datetime import datetime,timedelta


app= Flask(__name__)

connect = sqlite3.connect('database.db')
connect.execute('CREATE TABLE IF NOT EXISTS USERS(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                employee_id TEXT,name TEXT, cloth TEXT,\
                number INT,date DATE,pick_up DATE)')

@app.route('/' , methods=['POST','GET'])
def home():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        name=request.form.get('name')
        cloth= request.form.get('cloth')
        number = request.form.get('number')
        date = request.form.get('date')
        date_1 = datetime.strptime(date,'%Y-%m-%d')
        pick_up = date_1 + timedelta(days=2)
        final_pick_up= pick_up.weekday()
        if final_pick_up == 5 or final_pick_up==6:
            pick_up = pick_up + timedelta(days=2)
        pick_up = pick_up.strftime('%Y-%m-%d')
        '''pick_up = request.form.get('pick_up')'''
        with sqlite3.connect('database.db') as user:
            cursor= user.cursor()
            cursor.execute("INSERT INTO USERS(employee_id,name,cloth,number,date,pick_up) VALUES(?,?,?,?,?,?)", (employee_id, name,cloth,number,date,pick_up))
            user.commit()
    return render_template('index.html')

@app.route("/list")
def user_laundry():
    connect= sqlite3.connect('database.db')
    cursor= connect.cursor()
    cursor.execute('SELECT * FROM USERS')

    users= cursor.fetchall()
    return render_template("list_of_employee.html", users=users)
@app.route("/success")
def Success():
    return render_template('success.html')

if __name__ =='__main__':
    '''app.run(debug=True)'''
    app.run(host='192.168.19.32', port=5000)
