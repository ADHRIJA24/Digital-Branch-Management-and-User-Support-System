from flask import *
from database import*
user=Blueprint('user',__name__)

@user.route('/users')
def users():
    return render_template("user.html")

@user.route('/user_view')
def user_view():
    data={}
    a="SELECT * FROM USER INNER JOIN ACCOUNT USING(user_id) WHERE login_id='%s'"%(session['log'])
    data['view']=select(a)
    return render_template("user_view.html",data=data)

@user.route('/transaction')
def transaction():
    data={}
    a="select * from transaction where user_id='%s'"%(session['user']) 
    data['view']=select(a)
    return render_template("transaction.html",data=data)

@user.route('/balance')
def balance():
    data={}
    a="select * from account where user_id='%s'"%(session['user']) 
    data['view']=select(a)
    return render_template("balance.html",data=data)

@user.route('/complaint',methods=['POST','GET'])
def complaint():
    if 'submit' in request.form:
        complaint=request.form['complaint']
        qry="insert into complaint values(null,'%s','%s',curdate(),'pending')"%(session['user'],complaint)
        insert(qry)  
        return '''<script>alert("Successfully");window.location="/complaint"</script>''' 
    data={}
    q="select * from complaint where sender_id='%s'"%(session['user']) 
    r=select(q)
    data['view']=r
    return render_template("complaint.html",data=data)
    
@user.route('/feedback',methods=['POST','GET'])
def feedback():
    if 'submit' in request.form:
        feedback=request.form['feedback']
        qry="insert into feedback values(null,'%s','%s')"%(session['user'],feedback)
        insert(qry)  
        return '''<script>alert("Successfully");window.location="/feedback"</script>''' 
    data={}
    q="select * from feedback where sender_id='%s'"%(session['user']) 
    r=select(q)
    data['view']=r
    return render_template("feedback.html",data=data)
    