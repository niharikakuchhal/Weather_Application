from flask import Flask,render_template,request
from flask import redirect, flash, url_for
from flask import make_response, session,escape
import sqlite3 as sql
from weather import get_lat_lon,get_temp
import os

app = Flask(__name__)
app.secret_key = 'nhbahgbuBEIRGNUIueuiwiNJEnoi3i9jq8u6injgenilqheruoghaioenr'

def get_query(query):
    """
        Quering database
    """
    dbname='weather.db'
    con = sql.connect(dbname)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.commit()
    con.close()
    return result


@app.route('/')
def index():
    # email = request.cookies.get('email',None)
    email = session.get('email',None)
    if email:
        result = get_query(f'select name from user where email="{email}"')[0]
        cities = get_query(f"Select city from city where email='{email}' ")
        cities = [v[0] for v in cities ]
        data = []
        for city in cities:
            lat,lon = get_lat_lon(city)
            temp = get_temp(lat,lon)
            data.append(temp)
        if result:
            pass
        else:
            flash('Please Login Again')
        return render_template('weather.html',username=result[0],city= data)
    else:
        return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():
    email = request.form.get('email',None)
    password = request.form.get('password',None)
    if all([email,password]):
        email = email
        query = f'SELECT * from user where email = "{email}"'
        result = get_query(query) # ( ( 'email', 'password', 'name' ))
        if result:
            # user exixts check password
            db_password = result[0][1]
            if db_password == password:
                session.update(email=email)
                # resp = make_response(render_template('weather.html'))
                # resp.set_cookie('email',email)
                # return resp
                return redirect(url_for('index'))

            else:
                flash('Error! Invalid Password Please Try Again!')
            pass

        else:
            flash('Error! No Such Account Exists!')
            flash('Please Signup or check your login details ')
            return redirect(url_for('index'))
        # id, name, password, email

    else:
        flash('Error! Invalid Form Data! Please Try Again')
    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/mk_signup',methods=['POST'])
def mk_signup():
    name =request.form.get('name',None)
    email = request.form.get('email',None)
    password = request.form.get('password',None)
    if all([name,email,password]):
        name = name.strip().title()
        # result = get_query('select * from user where email=?',(email, ))
        try:
            con = sql.connect('weather.db')
            cursor = con.cursor()
            command = 'insert into user(email,password,name) values (?,?,?)'
            cursor.execute(command,(email,password,name))
            con.commit()
            flash("Account Successfully Created! Please Sign In")
            return redirect(url_for('index'))
        except sql.IntegrityError:
            flash('Error! Account Already Exists! Please Sign in')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error {e}')
            return redirect(url_for('index'))
                           
    else:
        flash('Error! Invalid Form Data! Please Check')

    return redirect(url_for('signup'))

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))
    # resp = make_response(render_template('login.html'))
    # resp.set_cookie('email',"")
    # return resp

@app.route('/add_city',methods=['POST'])
def add_city():
    email = session.get('email',None)
    if email:
        city = escape(request.form.get('city',None)).strip().lower()
        query = f'select * from city where email="{email}" AND city="{city}"'
        result = get_query(query)
        if result:
            flash('Error!City Already Exists!')
        else:
            coord = get_lat_lon(city)
            if coord:
                con = sql.connect('weather.db')
                cursor = con.cursor()
                query =f'INSERT INTO city values (?,?)'
                cursor.execute(query, (email,city))
                con.commit()
                cursor.close()
                con.close()
            else:
                flash('Error!Invalid City Name! City Not Found')
        return redirect(url_for('index'))
    flash('Error! Please Login First to Add City!')

@app.route('/delete/<name>')
def delete(name):
    email = session.get('email')
    if email:
        name = name.strip().lower()
        query = f'delete from city where email = "{email}" and city ="{name}"'
        get_query(query)
    
    else:
        flash('!Need to login first to Delete a Ciity!')
    return redirect(url_for('index'))

    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)