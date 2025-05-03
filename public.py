from flask import*
from database import *
public=Blueprint('public',__name__)
@public.route('/')
def home():
    return render_template("home.html")
@public.route('/login',methods=['POST','GET'])
def login():
    if 'submit' in request.form:
        uname=request.form['u']
        psw=request.form['p']
        print(uname,psw)
        z="select * from login where username='%s' and password='%s'"%(uname,psw)
        res=select(z)
        print(res,"///////")
        if res:
            session['log']=res[0]['login_id']
            if res[0]['usertype']=='admin':
                return redirect(url_for('admin.adm'))
            if res[0]['usertype']=='branch':
                qq="select * from branch where login_id='%s'"%(session['log'])
                rr=select(qq)
                if rr:
                    session['branch']=rr[0]['branch_id']
                    return redirect(url_for('branch.branch_home'))
            if res[0]['usertype']=='user':
                aa="select * from user where login_id='%s'"%(session['log'])
                bb=select(aa)
                if bb:
                    session['user']=bb[0]['user_id']
                    return redirect(url_for('user.users')) 

        else:
            return '''<script>alert(" invalid username or password");window.location="/login"</script>'''       
    return render_template("login.html")



# from datetime import datetime
# import numpy as np
# import tensorflow as tf
# import os



# # Model paths
# MODEL_PATH = os.path.join(os.path.dirname(__file__), 'static', 'model1.json')
# WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), 'static', 'model1.h5')

# print(f"Resolved MODEL_PATH: {MODEL_PATH}")
# print(f"Resolved WEIGHTS_PATH: {WEIGHTS_PATH}")
# print(f"Model path exists: {os.path.exists(MODEL_PATH)}")
# print(f"Weights path exists: {os.path.exists(WEIGHTS_PATH)}")
# print(f"TensorFlow version: {tf.__version__}")

# def load_model():
#     try:
#         print(f"Attempting to load model from {MODEL_PATH}")
#         if not os.path.exists(MODEL_PATH):
#             print(f"Error: Model file {MODEL_PATH} does not exist")
#             return None
#         if not os.path.exists(WEIGHTS_PATH):
#             print(f"Error: Weights file {WEIGHTS_PATH} does not exist")
#             return None
#         with open(MODEL_PATH, 'r') as json_file:
#             loaded_model_json = json_file.read()
#             print(f"Model JSON loaded, length: {len(loaded_model_json)}")
#         model = tf.keras.models.model_from_json(loaded_model_json)
#         print("Model architecture loaded successfully")
#         model.load_weights(WEIGHTS_PATH)
#         print("Model weights loaded successfully")
#         model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#         print("DOS detection model loaded and compiled successfully!")
#         return model
#     except Exception as e:
#         print(f"Error loading model: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return None

# dos_model = load_model()
# print(dos_model, "///////////////////////model")

# @public.route("/requests", methods=['POST', 'GET'])  # Changed from @public.route to @app.route
# def data():
#     ip = request.args.get('ip')
#     print(ip, "/////////////////////////////")
#     blocked_query = "SELECT * FROM blocked WHERE ipaddress='%s'" % ip
#     blocked_result = select(blocked_query)
#     if blocked_result:
#         return jsonify({"message": "blocked"})
#     insert_query = "INSERT INTO iprequest VALUES (null, '%s', CURDATE(), NOW())" % ip
#     insert(insert_query)
#     recent_query = "SELECT * FROM iprequest WHERE ipaddress='%s' AND date=CURDATE() ORDER BY iprequest_id DESC LIMIT 8" % ip
#     recent_requests = select(recent_query)
#     count_query = "SELECT COUNT(*) as request_count FROM iprequest WHERE ipaddress='%s' AND date=CURDATE()" % ip
#     count_result = select(count_query)
#     total_requests_today = count_result[0]['request_count'] if count_result else 0
#     if len(recent_requests) == 8:
#         row = []
#         current_time = datetime.now()
#         for req in recent_requests:
#             req_time_str = req['time']
#             if isinstance(req_time_str, str):
#                 req_time_obj = datetime.strptime(req_time_str, "%Y-%m-%d %H:%M:%S")
#             else:
#                 req_time_obj = req_time_str
#             time_diff = (current_time - req_time_obj).total_seconds()
#             row.append(time_diff)
#         print(row, "////row")
#         dos_detected = False
#         if dos_model is not None:
#             try:
#                 features = np.array(row).reshape(1, 8, 1)
#                 prediction = dos_model.predict(features)
#                 predicted_class = np.argmax(prediction, axis=1)[0]
#                 confidence = prediction[0][predicted_class]
#                 print(f"Model prediction: {'DOS Attack' if predicted_class == 1 else 'Normal Traffic'}")
#                 print(f"Confidence: {confidence:.4f}")
#                 if predicted_class == 1 or total_requests_today > 15:
#                     dos_detected = True
#                     print("Dos Attack Detected")
#             except Exception as e:
#                 print(f"Error during model prediction: {e}")
#         if dos_detected:
#             block_query = "INSERT INTO blocked (ipaddress) VALUES ('%s')" % ip
#             insert(block_query)
#             return jsonify({"message": "blocked"})
#     return jsonify({"message": "success"})


from flask import Blueprint, request, session, render_template, redirect
import logging

# Basic configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




@public.route('/s_log', methods=['GET', 'POST'])
def s_log():
    if request.method == 'POST':
        try:
            # Validate form data
            if 'u' not in request.form or 'p' not in request.form:
                logger.warning("Missing 'u' or 'p' in form data")
                return "<script>alert('Please fill in all fields.');window.location='/s_log'</script>"

            uname = request.form['u']
            psw = request.form['p']
            logger.info(f"Login attempt for username: {uname}")

            # Query the login table
            query = f"SELECT * FROM login WHERE username='{uname}' AND password='{psw}'"
            result = select(query)

            print(result, "//////////////////")

            if result:
                res1 = result[0]
                session['log'] = res1['login_id']

                if res1['usertype'] == 'admin':
                    return "<script>alert('login success');window.location='/adm'</script>"
                elif res1['usertype'] == 'branch':
                    query = f"SELECT * FROM branch WHERE login_id={session['log']}"
                    users = select(query)
                    if users:
                        session['branch'] = users[0]['branch_id']
                        return "<script>alert('login success');window.location='/branch_home'</script>"
                elif res1['usertype'] == 'user':
                    query = f"SELECT * FROM user WHERE login_id={session['log']}"
                    users = select(query)
                    if users:
                        session['user'] = users[0]['user_id']
                        return "<script>alert('login success');window.location='/users'</script>"
            else:
                logger.warning(f"Failed login attempt for username: {uname}")
                return "<script>alert('Login failed. Please try again.');window.location='/s_log'</script>"

        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return "<script>alert('An error occurred. Please try again.');window.location='/s_log'</script>"

    return render_template('login.html')





@public.route('/s_home')
def s_home():


    return render_template('home.html')