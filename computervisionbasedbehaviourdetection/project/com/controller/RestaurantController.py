import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template

from project import app
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RestaurantDAO import RestaurantDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RestaurantVO import RestaurantVO


@app.route('/user/loadRestaurant', methods=['GET'])
def userLoadRestaurant():
    try:
        areaDAO = AreaDAO()
        areaVOlist = areaDAO.viewArea()
        return render_template("user/register.html", areaVOlist=areaVOlist)
    except Exception as ex:
        print(ex)


@app.route('/user/insertRestaurant', methods=['POST'])
def userInsertRestaurant():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        restaurantVO = RestaurantVO()
        restaurantDAO = RestaurantDAO()

        loginUsername = request.form['loginUsername']
        restaurantName = request.form['restaurantName']
        restaurantNumber = request.form['restaurantNumber']
        restaurantOwner = request.form['restaurantOwner']

        restaurant_AreaId = request.form['restaurant_AreaId']
        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "cvisiondetection@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "cvision@123")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        restaurantVO.restaurantName = restaurantName
        restaurantVO.restaurantNumber = restaurantNumber
        restaurantVO.restaurantOwner = restaurantOwner
        restaurantVO.restaurant_AreaId = restaurant_AreaId
        restaurantVO.restaurant_LoginId = loginVO.loginId

        restaurantDAO.insertRestaurant(restaurantVO)

        return render_template("user/login.html")

    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewUser():
    try:
        restaurantDAO = RestaurantDAO()
        userVOList = restaurantDAO.viewUser()
        return render_template('admin/viewUser.html', userVOList=userVOList)

    except Exception as ex:
        print(ex)
