from datetime import datetime, date

from flask import request, render_template, session, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/user/loadFeedback', methods=['GET'])
def userPostFeedback():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addFeedback.html')
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']
            feedbackFrom_LoginId = session.get('session_loginId')

            feedbackDate = str(date.today())
            feedbackTime = str(datetime.now().strftime("%H:%M:%S"))

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback', methods=['GET'])
def userViewFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            loginId = session.get('session_loginId')
            userName = session.get('session_loginUsername')

            feedbackVO.feedbackFrom_LoginId = loginId

            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList, userName=userName)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackVO.feedbackId = feedbackId

            feedbackDAO.deleteFeedback(feedbackVO)
            return redirect(url_for('userViewFeedback'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()

            feedbackVOList = feedbackDAO.adminViewFeedback()

            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/updateFeedback', methods=['GET'])
def adminUpdateFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackVO.feedbackId = feedbackId

            feedbackTo_loginID = session.get('session_loginId')
            feedbackVO.feedbackTo_LoginId = feedbackTo_loginID

            feedbackDAO.updateFeedback(feedbackVO)
            return redirect(url_for('adminViewFeedback'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)
