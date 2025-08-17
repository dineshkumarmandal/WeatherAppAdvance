from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import re
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = '799f2734d0863b14196ec025d94d2dca'

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def get_coordinates(city_name):
    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}'
    response = requests.get(geo_url)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data['lat'], data['lon'], data['name']
    return None, None, None

 
# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'weatherappadvance'



mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
     return render_template('view.html')


@app.route('/view')
def view_locations():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM location_details")
    columns = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    assoc_result = [dict(zip(columns, row)) for row in result]
    cur.close()
    return render_template('view.html', locations=assoc_result)


@app.route('/add', methods=['POST', 'GET'])
def add_location():
    error_message = None
    success_message = None
    if request.method == 'POST':
        zip_code = request.form['zip_code'].strip()
        landmarks = request.form['landmarks'].strip()
        emailId = request.form['emailId'].strip()
        city = request.form['city'].strip()
        country = request.form['country'].strip()
        forecast_start_date = request.form['forecast_start_date'].strip()
        forecast_end_date = request.form['forecast_end_date'].strip()
        id = request.form['id'].strip()
        # Server-side validation
        if not emailId or not forecast_start_date or not forecast_end_date or not city:
            error_message="Fields are required."
        elif not is_valid_email(emailId):
            error_message = "Invalid email format."
        else :
            #Convert date strings from the form to datetime objects
            start_date = datetime.strptime(forecast_start_date, '%Y-%m-%d')
            end_date = datetime.strptime(forecast_end_date, '%Y-%m-%d')
            #Check for a valid date rang
            if start_date>end_date:
                error_message = "Start date cannot be after the end date."
            
            #Show Message if any validation failed to user
            if error_message:
                return render_template('add.html', error=error_message, loc={})
            

            lat, lon, city = get_coordinates(city)

            #Update Data
            if id :
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE location_details
                    SET LATITUDE = %s, LONGITUDE = %s, LANDMARKS = %s, CITY = %s, COUNTRY = %s, ZIP_CODE = %s, FORECAST_START_DATE = %s, FORECAST_END_DATE = %s, EMAIL_ID = %s
                    WHERE ID = %s
                """, (lat, lon, landmarks, city, country, zip_code, forecast_start_date, forecast_end_date, emailId, id))
                mysql.connection.commit()
                cur.close()
                success_message = "Location details updated successfully!"
                #return redirect('/view')
                return render_template('add.html', success=success_message, loc={})
            else:
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO location_details (LATITUDE, LONGITUDE, LANDMARKS, CITY, COUNTRY, ZIP_CODE, FORECAST_START_DATE, FORECAST_END_DATE, EMAIL_ID)
                    VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)
                """, (lat, lon, landmarks, city, country, zip_code, forecast_start_date, forecast_end_date, emailId))
                mysql.connection.commit()
                cur.close()
                success_message = "Location details saved successfully!"
                #return redirect('/view')
                return render_template('add.html', success=success_message, loc={})

    return render_template('add.html', loc={})
    

@app.route('/success')
def success():
    return "Location details saved successfully!"

@app.route('/delete/<int:id>')
def delete_location(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM location_details WHERE ID=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/view')

@app.route('/edit/<int:id>')
def edit_location(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM location_details WHERE ID=%s", (id,))
    result = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    assoc_result = dict(zip(columns, result))
    cur.close()
    return render_template('add.html', loc=assoc_result)



if __name__ == '__main__':
    app.run(debug=True)