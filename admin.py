from flask import*
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adm')
def adm():

    return render_template("admin.html")
    
@admin.route('/admin_view')
def admin_view():
    data={}
    a="select * from user"
    data['view']=select(a)


    return render_template("admin_view_user.html",data=data)


@admin.route('/admin_view_complaints')
def admin_view_complaints():
    data={}
    a="select * from complaint"
    data['view']=select(a)

    return render_template("admin_view_complaints.html",data=data)


@admin.route('/reply',methods={'POST','GET'})
def reply():
    complaint_id=request.args['id']
    if 'submit' in request.form:
        reply=request.form['r']
        print(reply)
        q="update complaint set reply='%s' where complaint_id='%s'"%(reply,complaint_id)
        update(q)
        return '''<script>alert("success");window.location="/admin_view_complaints"</script>'''

    return render_template("reply.html")



@admin.route('/admin_branch',methods=['POST','GET'])
def admin_branch():
    if 'submit' in request.form:
        uname=request.form['u']
        name=request.form['name']
        place=request.form['place']

        phone=request.form['phone']
        code=request.form['code']
        post=request.form['post']
        pin=request.form['pin']

        email=request.form['email']
        psw=request.form['p']

        print(uname,psw,phone,name,email,place,code,post,pin)

        qry2="insert into login values(null,'%s','%s','branch')"%(uname,psw)
        res=insert(qry2)

        qry="insert into branch values(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(res,name,place,phone,code,email,post,pin)
        insert(qry)  

        return '''<script>alert("Registered Successfully");window.location="/admin_branch"</script>''' 

    data={}
    q="select * from branch" 
    r=select(q)
    data['view']=r

    return render_template("admin_branch.html",data=data)
    
@admin.route('/admin_notification',methods=['POST','GET'])
def admin_notification():
    if 'submit' in request.form:
        title=request.form['title']
        description=request.form['description']
        date=request.form['date']
        qry="insert into notification values(null,'%s','%s',curdate())"%(title,description)
        insert(qry)
 
       
    data={}
    a="select * from notification"
    res=select(a)
    if res:
        data['notification']=res
       

    return render_template("admin_notification.html",data=data)

@admin.route('/feedback_view')
def feedbac_view():
    data={}
    a="select * from feedback"
    data['view']=select(a)

    return render_template("feedback_view.html",data=data)