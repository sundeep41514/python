from flask import Flask, render_template, request, redirect, url_for
import yaml, random, re, sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)

with open("myown.yml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

a,Username,main_hash = 1,"",{}

@app.route("/")
@app.route("/home")
def home():
    global a,Username,main_hash
    if a == 1:
        return redirect(url_for('login'))
    a = 1
    main_hash.update({Username:[]})

    bcrypt = Bcrypt()
    key = bcrypt.generate_password_hash('testing').decode('utf-8')

    conn = sqlite3.connect("RandF_accounts.sqlite")
    cur = conn.cursor()
    cur.execute('update Accounts set key = "{!s}" where Username = "{!s}";'.format(key, Username))
    conn.commit()

    return render_template("index.html",username= Username, key=key)

@app.route("/get")
def get_bot_response():

    global data_loaded,main_hash
    main_arr = None
    main_userText = request.args.get('msg').split("@")
    userText = main_userText[0]
    username = main_userText[1]
    key_value = main_userText[2]

    conn = sqlite3.connect("RandF_accounts.sqlite")
    cur = conn.cursor()
    cur.execute('select * from Accounts')
    val = cur.fetchall()

    for x in val:
        if x[0] == username and x[2] == key_value:
            main_arr = main_hash[username]

    if main_arr == None:
        return "exit"

    ########################### Sample texts like HI, BYE ###########################################
    for x in data_loaded:
        if x == 'conversations':
            for val in data_loaded[x]:
                if re.search(userText.lower(),val[0].lower()):
                    print(main_hash)
                    return (val[random.randint(1, len(val) - 1)])
                elif re.search(val[0].lower(),userText.lower()):
                    print(main_hash)
                    return (val[random.randint(1, len(val) - 1)])

    return "I dont know what to say"

@app.route('/login', methods=['GET', 'POST'])
def login():
    global a,Username
    conn = sqlite3.connect("RandF_accounts.sqlite")
    cur = conn.cursor()
    error = None
    cur.execute('select * from Accounts')
    temp = cur.fetchall()

    if request.method == 'POST':
        for val in temp:
            if request.form['username'] == val[0] and request.form['password'] == val[1]:
                a,Username = 0,request.form['username']
                return redirect(url_for('home'))
            else:
                error = 'Invalid credentials.'

    return render_template('login_testing.html', error=error)

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='chat_bot_error.log', level=logging.DEBUG)
    app.run(debug=True, host="localhost", port=3456, threaded= True)