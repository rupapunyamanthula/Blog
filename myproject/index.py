from flask import *
import mysql.connector
from flask_ngrok import run_with_ngrok
import os
import csv


app=Flask(__name__)#object creation for flask
'''run_with_ngrok(app)'''
app.secret_key="dnt tell" # for flash or alert messgae
UPLOAD_FOLDER='./static/data'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="blog"
)

@app.route("/admin",methods=['GET','POST'])
def admin():
	if request.method=="POST":
		uname=request.form['uname']
		pwd=request.form['pwd']
		cur=myconn.cursor()
		cur.execute("""select * from admin where 
			username1=%s and Password1=%s""",(uname,pwd))
		data=cur.fetchall()
		if data:
			session['loggedadmin']=True
			flash("Admin Login Successfully")
			return render_template("admin.html")

		else:
			flash("Incorrect Username or Password")
	return render_template("login1.html")
@app.route("/accept",methods=['GET','POST'])
def accept():
	if not session.get('loggedadmin'):
		return render_template("login1.html")
	if request.method == "POST":
		id=request.form['accept']
		cur=myconn.cursor()
		cur.execute("update new1 set status='0' where sno=%s"%(id))
		myconn.commit()
		return render_template("admin.html")
@app.route("/adminpen",methods=['GET','POST'])
def adminpen():
	if not session.get('loggedadmin'):
		return render_template("login1.html")
	else:
		cur=myconn.cursor()
		cur.execute("select * from new1 where status='1'")
		data=cur.fetchall()
		return render_template("display1.html",data=data)
 # index page or first page
@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
		uname=request.form['uname']
		pwd=request.form['pwd']
		cur=myconn.cursor()
		cur.execute("""select * from users where 
			Email=%s and Password=%s""",(uname,pwd))
		data=cur.fetchall()
		if data:
			session['loggedin']=True
			session['user']=uname
			session['name']=data[0][1]

			flash("Login Successfully")
			return render_template("index1.html")

		else:
			flash("Incorrect Username or Password")
	return render_template("login.html")

@app.route("/")
@app.route("/home")
def home():
	cur=myconn.cursor()
	cur.execute("select * from new1 where status='0' order by sno desc")
	data=cur.fetchall()
	return render_template("index.html",data=data)
@app.route("/display/<sno>")	
def display(sno):
	cur=myconn.cursor()
	cur.execute("select * from new1 where sno=%s",(sno,))
	data=cur.fetchall()
	return render_template("display.html",data=data)

@app.route("/register",methods=['GET','POST'])
def register():

	if request.method == "POST":

		name=request.form['name']
		email=request.form['email']
		phno=request.form['phno']
		
		gen=request.form['gender']
	
		password=request.form['password']
		genre=request.form['genre']
		mycur=myconn.cursor()
		mycur.execute("select * from users where Email=%s",(email,))
		data=mycur.fetchall()
		if(len(data)==0):
			mycur.execute("""insert into users(Name,Email,Phoneno,Gender,Password,Genre)
				values(%s,%s,%s,%s,%s,%s)""",
				(name,email,phno,gen,password,genre))
			myconn.commit()
			flash("Registered Successfully")
		else:
			flash("Already Registered")


		

		return redirect(url_for('register'))

	else:
		return render_template("about.html")

@app.route("/userpanel",methods=['GET','POST'])
def userpanel():
	if not session.get('loggedin'):
		return render_template("login.html")
	return render_template("index1.html")




@app.route("/view",methods=['GET','POST'])
def view():
	if not session.get('loggedin'):
		return render_template("login.html")

	cur=myconn.cursor()
	cur.execute("select * from new1 where author=%s",(session['user'],))
	data=cur.fetchall()
	if len(data)==0:
		return "Sorry!!You've Not Created Any Books Yet!!"
	else:
		return render_template("view.html",data=data)


@app.route("/delete",methods=['GET','POST'])
def delete():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['delete']
		cur=myconn.cursor()
		cur.execute("delete from new1 where sno=%s"%(id))
		myconn.commit()
		flash("Deleted Successfully")
		return redirect(url_for('view'))


@app.route("/edit",methods=['GET','POST'])
def edit():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['edit']
		cur=myconn.cursor()
		cur.execute("select * from new1 where sno=%s"%(id))
		data=cur.fetchall()
		return render_template("edit.html",data=data)

@app.route("/update",methods=['GET','POST'])
def update():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['id']
		name=request.form['title']
		email=request.form['content']
		phno=request.form['tags']
		mycur=myconn.cursor()
		mycur.execute("""update new1 set title=%s,
			content=%s,tags=%s where sno=%s""",
			(name,email,phno,id))
		myconn.commit()
		return redirect(url_for('view'))
@app.route("/new",methods=['GET','POST'])	
def new():
	if request.method == "POST":

		title=request.form['title']
		content=request.form['content']
		tags=request.form['tags']
		author=session['user']
		
		
		mycurr=myconn.cursor()
		mycurr.execute("select Name from users where Email=%s",(author,))
		data=mycurr.fetchall()
		mycurr.execute("""insert into new1(title,content,tags,author,name)
				values(%s,%s,%s,%s,%s)""",
				(title,content,tags,author,data[0][0]))

		myconn.commit()
		flash("Submitted content Successfully")
    
	else:
		return render_template("new.html")
	return redirect(url_for('new'))


@app.route("/logout")
def logout():
	session['loggedin']=False
	return render_template("index.html")
@app.route("/logoutadmin")
def logoutadmin():
	session['loggedadmin']=False
	return render_template("index.html")

# last lines
if __name__ =="__main__":
	app.run(debug=True)


