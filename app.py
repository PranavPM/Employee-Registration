from flask import Flask, render_template, request
import sqlite3 as sql
import os
app = Flask(__name__)


UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
UPLOAD_FOLDER = '/path/to/the/uploads'
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
            if request.method == 'POST':
                  if 'file' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                  file = request.files['file']
                              
                  if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)                  

                  if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        os.rename =(filename , empid)     
                    
            
      except :
         con.rollback()
         msg = "Try again"

      finally:         
         return render_template("notregistered.html",msg = msg)
         con.close()
                 