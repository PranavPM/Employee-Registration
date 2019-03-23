from flask import Flask, render_template, request
import sqlite3 as sql
import os
app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['jpg', 'gif', 'png'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
       conn = sql.connect('database.db')
       conn.execute('CREATE TABLE if not EXISTS invited (empid TEXT not null unique, acn INTEGER not null check(acn between 0 and 99999))')
       conn.close()
       return render_template('home.html')

@app.route('/upimg',methods = ['POST', 'GET'])       
def upload():
    if request.method == 'POST':
         if request.form['file'] == 'file':
                  target = os.path.join(UPLOAD_FOLDER, 'images/')

                  if not os.path.isdir(target):
                        os.mkdir(target)

                  for file in request.files.getlist("file"):

                        filename = file.filename
                        destination = "/".join([target, filename])

                        file.save(destination)
                        msg = "Image Uploaded"
                        break
                  render_template("notregistered.html", msg=msg)

     

@app.route('/emp',methods = ['POST', 'GET'])
def emp():
   if request.method == 'POST':
      try:
            empid = request.form['empid']  
            acn = request.form['acn']

            with sql.connect("database.db") as con:
                con.execute('INSERT INTO registry VALUES (?,?)',(empid,acn) )
                msg = "Entry successful. \nThank you!!"
                con.commit()          
                                
      except :
         con.rollback()
         msg = "Try again"

      finally:   
            con.close()      
            return render_template("notregistered.html",msg = msg)
         
                 
if __name__ == '__main__':
         app.debug = True
         app.run(port=4555)

