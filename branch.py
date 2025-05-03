from flask import *
from database import*
import uuid
branch=Blueprint('branch',__name__)

@branch.route('/branch_home')
def branch_home():

    return render_template("branch.html")

@branch.route('/branch_view')
def branch_view():

    return render_template("branch_view_user.html")

@branch.route('/branch_notification',methods=['POST','GET'])
def branch_notification():
    if 'submit' in request.form:
        title=request.form['title']
        description=request.form['description']
        date=request.form['date'] 
    data={}
    a="select * from notification"
    res=select(a)
    if res:
        data['notification']=res
    return render_template("branch_notification.html",data=data)



@branch.route('/branch_view_user',methods=['POST','GET'])
def branch_view_user():
    if 'submit' in request.form:
        name=request.form['name']
        photo=request.form['photo']
        phone=request.form['phone'] 
        place=request.form['place'] 
        pin=request.form['pin']
        gender=request.form['gender'] 
        age=request.form['age'] 
        id_proof=request.form['id_proof'] 
        email=request.form['email'] 
    data={}
    a="select * from user where branch_id='%s'"%(session['branch'])
    res=select(a)
    if res:
        data['user']=res
    return render_template("branch_view_user.html",data=data)

@branch.route('/branch_account',methods=['POST','GET'])
def branch_account():
    # if 'submit' in request.form:
    #     account_no=request.form['account_no']
    #     ifsc_code=request.form['ifsc_code']
    #     branch=request.form['branch'] 
    #     branch_amount=request.form['branch_amount'] 
    #     print(account_no,ifsc_code,branch,branch_amount)
    #     qry="insert into account values(null,'%s','%s','%s','%s')"%(account_no,ifsc_code,branch,branch_amount)
    #     insert(qry)  

    data={}
    a="select * from account where branch_id='%s'"%(session['branch']) 
    res=select(a)
    if res:
        data['account']=res
    return render_template("branch_account.html",data=data)




@branch.route('/Deposit',methods=['POST','GET'])
def Deposit():
    id=request.args['id']
    acc_id=request.args['acc_id']
    if 'submit' in request.form:
        amount=request.form['amount']
        transfer_type=request.form['type']
        date=request.form['date']

        print(amount,"(((((((((())))))))))")

        if transfer_type == 'deposit':
            qry="insert into transaction values(null,'%s','%s','%s',curdate())"%(id,amount,transfer_type)
            insert(qry)

            qry1="update account set balance_amount=(balance_amount + '%s') where account_id='%s'"%(float(amount),acc_id)
            update(qry1)

            print(qry1)

        if transfer_type == 'withdrawal':
            qry="insert into transaction values(null,'%s','%s','%s',curdate())"%(id,amount,transfer_type)
            insert(qry)

            qry1="update account set balance_amount=(balance_amount - '%s') where account_id='%s'"%(float(amount),acc_id)
            update(qry1)


    data={}
    a="select * from transaction"
    res=select(a)
    if res:
        data['transaction']=res
    return render_template("deposit.html",data=data)

# @branch.route('/withdrawal',methods=['POST','GET'])
# def withdrawal():
#     id=request.args['id']
#     if 'submit' in request.form:
#         amount=request.form['amount']
#         type=request.form['type']
#         date=request.form['date']
#         qry="insert into transaction values(null,'%s','%s','%s',curdate())"%(id,amount,type)
#         insert(qry)
#     data={}
#     a="select * from transaction"
#     res=select(a)
#     if res:
#         data['transaction']=res
       

#     return render_template("withdrawal.html",data=data)

@branch.route('/register',methods=['POST','GET'])
def register():

    data={}
    q="select * from branch"
    r=select(q)
    data['view']=r

    if 'submit' in request.form:
        name=request.form['name']
        Photo=request.files['Photo']
        Phone=request.form['Phone']
        place=request.form['place']
        pin=request.form['pin']
        gender=request.form['gender']
        age=request.form['age']
        id_proof=request.files['id_proof']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        branchs=request.form['branchs']
        print(name,Photo,Phone,place,pin,gender,age,id_proof,email,username,password)

        path='static/'+str(uuid.uuid4())+Photo.filename
        Photo.save(path)
        path1='static/'+str(uuid.uuid4())+id_proof.filename
        id_proof.save(path1)

        qry2="insert into login values(null,'%s','%s','user')"%(username,password)
        rea=insert(qry2)

        qry="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(rea,branchs,name,path,Phone,place,pin,gender,age,path1,email)
        insert(qry)
        return '''<script>alert("Registered Successfully");window.location="/register"</script>''' 
        
    return render_template("register.html",data=data)

@branch.route('/account',methods=['POST','GET'])
def account():
    id=request.args['id']
    if 'submit' in request.form:
        account_no=request.form['account_no']
        ifsc_code=request.form['ifsc_code']
        branch=request.form['branch']
        balanace_amount=request.form['balance_amount']
        print(account_no,ifsc_code,branch,balanace_amount)

        qry="insert into account values(null,'%s','%s','%s','%s','%s','%s')"%(id,session['branch'],account_no,ifsc_code,branch,balanace_amount)
        insert(qry)  

        return '''<script>alert("Registered Successfully");window.location="/branch_view_user"</script>''' 

    data={}
    q="select * from account" 
    r=select(q)
    data['view']=r

    return render_template("account.html",data=data)