import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, session, redirect, url_for, jsonify

from project import app
from project.com.controller.RestaurantController import adminViewUser
from project.com.dao.BranchDAO import BranchDAO
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegionFourDAO import RegionFourDAO
from project.com.dao.RegionOneDAO import RegionOneDAO
from project.com.dao.RegionThreeDAO import RegionThreeDAO
from project.com.dao.RegionTwoDAO import RegionTwoDAO
from project.com.dao.RestaurantDAO import RestaurantDAO
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.BranchVO import BranchVO
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegionFourVO import RegionFourVO
from project.com.vo.RegionOneVO import RegionOneVO
from project.com.vo.RegionThreeVO import RegionThreeVO
from project.com.vo.RegionTwoVO import RegionTwoVO
from project.com.vo.VideoVO import VideoVO


@app.route('/')
def adminLoadLogin():
    try:
        print("in login")
        session.clear()
        return render_template('user/login.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/validateLogin', methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        print(loginUsername)
        loginPassword = request.form['loginPassword']
        print(loginPassword)

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]
        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:
            msg = "Username or Password is incorrect"
            return render_template('user/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == "inactive":
            blockMsg = "This user is temporarily blocked"
            return render_template('user/login.html', error=blockMsg)

        else:
            for row in loginDictList:
                if row['loginStatus'] == "active":
                    loginId = row['loginId']
                    loginUsername = row['loginUsername']
                    loginRole = row['loginRole']
                    print(loginRole)

                    session['session_loginId'] = loginId
                    session['session_loginUsername'] = loginUsername
                    session['session_loginRole'] = loginRole

                    session.permanent = True

                    if loginRole == 'admin':
                        return redirect(url_for('adminLoadDashboard'))
                    elif loginRole == 'user':
                        return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'user':

                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            complainCount = 0
            userCount = 0
            feedbackCount = 0
            branchCount = 0
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainStatus = 'Pending'
            complainVO.complainStatus = complainStatus
            complainVOList = complainDAO.adminViewComplain(complainVO)
            print(len(complainVOList))
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.adminViewFeedback()
            print(len(feedbackVOList))
            branchDAO = BranchDAO()
            branchVOList = branchDAO.adminViewBranch()
            print(len(branchVOList))
            restaurantDAO = RestaurantDAO()
            userVOList = restaurantDAO.viewUser()
            print(len(userVOList))
            for i in complainVOList:
                complainCount = complainCount + 1
            for i in feedbackVOList:
                feedbackCount = feedbackCount + 1
            for i in branchVOList:
                branchCount = branchCount + 1
            for i in userVOList:
                userCount = userCount + 1

            restaurantList = [i[0] for i in userVOList]

            return render_template('admin/index.html', complainCount=complainCount,
                                   feedbackCount=feedbackCount,
                                   branchCount=branchCount, userCount=userCount, restaurantList=restaurantList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            complainPendingCount = 0
            complainRepliedCount = 0
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainStatus = 'Pending'
            complainVO.complainStatus = complainStatus
            complainVO.complainFrom_LoginId = session.get('session_loginId')
            complainVOList = complainDAO.viewComplainStatus(complainVO)
            complainVO2 = ComplainVO()
            complainRepliedStatus = 'Replied'
            complainVO2.complainFrom_LoginId = session.get('session_loginId')
            complainVO2.complainStatus = complainRepliedStatus
            complainList = complainDAO.viewComplainStatus(complainVO2)
            for i in complainVOList:
                complainPendingCount = complainPendingCount + 1
            for i in complainList:
                complainRepliedCount = complainRepliedCount + 1

            feedbackReviewedCount = 0
            feedbackActiveCount = 0
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()
            loginId = session.get('session_loginId')
            feedbackVO.feedbackFrom_LoginId = loginId
            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)
            for i in feedbackVOList:
                if i.feedbackTo_LoginId == None:
                    feedbackActiveCount = feedbackActiveCount + 1
                else:
                    feedbackReviewedCount = feedbackReviewedCount + 1

            return render_template('user/index.html', complainPendingCount=complainPendingCount,
                                   complainRepliedCount=complainRepliedCount,
                                   feedbackReviewedCount=feedbackReviewedCount,
                                   feedbackActiveCount=feedbackActiveCount)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['GET'])
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')
            loginVO.loginId = loginId

            loginVO.loginStatus = 'active'
            loginDAO.updateLogin(loginVO)

            return adminViewUser()
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')
            loginVO.loginId = loginId
            loginVO.loginStatus = 'inactive'

            loginDAO.updateLogin(loginVO)

            return adminViewUser()
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/admin/forgotPassword")
def adminForgotPassword():
    try:
        return render_template("user/forgotPassword.html")
    except Exception as ex:
        print(ex)


@app.route("/admin/insertUsername", methods=["post"])
def adminInsertUsername():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUsername = request.form['loginUsername']
        loginVO.loginUsername = loginUsername
        loginVOList = loginDAO.validateLoginUsername(loginVO)
        loginDictList = [i.as_dict() for i in loginVOList]
        lenLoginDictList = len(loginDictList)
        if lenLoginDictList == 0:
            msg = "E - mail does not exist !"
            return render_template("user/forgotPassword.html", msg=msg)
        else:
            for row1 in loginDictList:
                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

            otp = ''.join((random.choice(string.digits)) for x in range(6))

            sender = "cvisiondetection@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "Reset Password"

            msg.attach(MIMEText(otp, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "cvision@123")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            session["otp"] = otp
            return render_template("user/addOTP.html")


    except Exception as ex:
        print(ex)


@app.route("/admin/insertOtp", methods=['post'])
def adminInsertOtp():
    try:

        loginOtp = request.form["loginOtp"]
        if session["otp"] == loginOtp:
            return render_template("user/addNewPassword.html")
        else:
            msg = "Otp does not Match!"
            return render_template("user/addOTP.html", msg=msg)
    except Exception as ex:
        print(ex)


@app.route("/admin/insertNewPassword", methods=['post'])
def adminInsertNewPassword():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()
        loginPassword = request.form["loginPassword"]

        sender = "cvisiondetection@gmail.com"

        receiver = session["session_loginUsername"]

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "New Password"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "cvision@123")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        server.quit()

        loginVO.loginId = session['session_loginId']
        loginVO.loginPassword = loginPassword
        loginDAO.loginUpdateUser(loginVO)
        return render_template("user/login.html")

    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadBranchByRestaurant', methods=['GET'])
def adminAjaxLoadBranchByRestaurant():
    try:
        if adminLoginSession() == 'admin':
            restaurantId = request.args.get('restaurantId')

            branchVO = BranchVO()
            branchDAO = BranchDAO()

            branchVO.branch_RestaurantId = restaurantId
            branchVOList = branchDAO.viewBranch(branchVO)

            ajaxBranchJson = [i[0].as_dict() for i in branchVOList]
            print('ajaxBranchJson>>>>>', ajaxBranchJson)

            return jsonify(ajaxBranchJson)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadVideoByBranch', methods=['GET'])
def adminAjaxLoadVideoByBranch():
    try:
        if adminLoginSession() == 'admin':
            branchId = request.args.get('branchId')

            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoVO.video_BranchId = branchId
            videoVOList = videoDAO.viewVideoByBranch(videoVO)

            ajaxVideoJson = [i.as_dict() for i in videoVOList]

            print('ajaxVideoJson>>>>>', ajaxVideoJson)

            return jsonify(ajaxVideoJson)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadGraphByVideo', methods=['GET'])
def adminLoadGraphByVideo():
    try:
        if adminLoginSession() == 'admin':
            videoId = request.args.get('videoId')

            regionOneVO = RegionOneVO()
            regionOneDAO = RegionOneDAO()
            regionOneVO.regionOne_VideoId = videoId
            regionOneVOList = regionOneDAO.regionOnePersonCount(regionOneVO)
            regionOneCount = regionOneVOList.regionOnePersonCount
            print('regionOneCount>>>>>>>>', regionOneVOList.regionOnePersonCount)

            regionTwoVO = RegionTwoVO()
            regionTwoDAO = RegionTwoDAO()
            regionTwoVO.regionTwo_VideoId = videoId
            regionTwoVOList = regionTwoDAO.regionTwoPersonCount(regionTwoVO)
            regionTwoCount = regionTwoVOList.regionTwoPersonCount
            print('regionTwoCount>>>>>>>>', regionTwoVOList.regionTwoPersonCount)

            regionThreeVO = RegionThreeVO()
            regionThreeDAO = RegionThreeDAO()
            regionThreeVO.regionThree_VideoId = videoId
            regionThreeVOList = regionThreeDAO.regionThreePersonCount(regionThreeVO)
            regionThreeCount = regionThreeVOList.regionThreePersonCount
            print('regionThreeCount>>>>>>>>', regionThreeVOList.regionThreePersonCount)

            regionFourVO = RegionFourVO()
            regionFourDAO = RegionFourDAO()
            regionFourVO.regionFour_VideoId = videoId
            regionFourVOList = regionFourDAO.regionFourPersonCount(regionFourVO)
            regionFourCount = regionFourVOList.regionFourPersonCount
            print('regionFourCount>>>>>>>>', regionFourVOList.regionFourPersonCount)

            graphList = []

            if regionOneCount is not None:
                regionOne = {'regionName': 'RegionOne', 'personCount': int(regionOneCount)}
                graphList.append(regionOne)
            else:
                regionOne = {'regionName': 'RegionOne', 'personCount': 0}
                graphList.append(regionOne)

            if regionTwoCount is not None:
                regionTwo = {'regionName': 'RegionTwo', 'personCount': int(regionTwoCount)}
                graphList.append(regionTwo)
            else:
                regionTwo = {'regionName': 'RegionTwo', 'personCount': 0}
                graphList.append(regionTwo)

            if regionThreeCount is not None:
                regionThree = {'regionName': 'RegionThree', 'personCount': int(regionThreeCount)}
                graphList.append(regionThree)
            else:
                regionThree = {'regionName': 'RegionThree', 'personCount': 0}
                graphList.append(regionThree)

            if regionFourCount is not None:
                regionFour = {'regionName': 'RegionFour', 'personCount': int(regionFourCount)}
                graphList.append(regionFour)
            else:
                regionFour = {'regionName': 'RegionFour', 'personCount': 0}
                graphList.append(regionFour)

            response = {'responseKey': graphList}

            return jsonify(response)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
