import os
from datetime import datetime, date

from flask import request, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route('/user/loadComplain', methods=['GET'])
def userPostComplain():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addComplain.html')
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            UPLOAD_FOLDER = 'project/static/userResources/complainAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            file = request.files['complainFilename']
            print(file)

            complainFileName = secure_filename(file.filename)
            print("complainFileName >>>>>>>>>>>>>>>>>>>>>>. ", complainFileName)

            if complainFileName != "":
                complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
                print(complainFilePath)

                file.save(os.path.join(complainFilePath, complainFileName))

                complainFrom_LoginId = session.get('session_loginId')
                complainStatus = 'Pending'
                complainDate = str(date.today())
                complainTime = str(datetime.now().strftime("%H:%M:%S"))

                complainVO = ComplainVO()
                complainDAO = ComplainDAO()

                complainVO.complainSubject = complainSubject
                complainVO.complainDescription = complainDescription
                complainVO.complainDate = complainDate
                complainVO.complainTime = complainTime
                complainVO.complainStatus = complainStatus
                complainVO.complainFrom_LoginId = complainFrom_LoginId
                complainVO.complainFileName = complainFileName
                complainVO.complainFilePath = complainFilePath.replace('project', '..')

                complainDAO.insertComplain(complainVO)
            else:
                print('photo does not exist')

                complainFileName = "None"
                complainFilePath = "None"

                complainFrom_LoginId = session.get('session_loginId')
                complainStatus = 'Pending'
                complainDate = str(date.today())
                complainTime = str(datetime.now().strftime("%H:%M:%S"))

                complainVO = ComplainVO()
                complainDAO = ComplainDAO()

                complainVO.complainSubject = complainSubject
                complainVO.complainDescription = complainDescription
                complainVO.complainDate = complainDate
                complainVO.complainTime = complainTime
                complainVO.complainStatus = complainStatus
                complainVO.complainFrom_LoginId = complainFrom_LoginId
                complainVO.complainFileName = complainFileName
                complainVO.complainFilePath = complainFilePath.replace('project', '..')

                complainDAO.insertComplain(complainVO)

            return redirect(url_for('userViewComplain'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['GET'])
def userViewComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainFrom_LoginID = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginID
            userName = session.get('session_loginUsername')
            print("just before complain query ....... ")
            complainVOList = complainDAO.viewComplain(complainVO)
            print("after queryyy.......", complainVOList)
            return render_template('user/viewComplain.html', complainVOList=complainVOList, userName=userName)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['GET'])
def userViewComplainReply():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            userName = 'Admin'

            complainVOList = complainDAO.viewComplainReply(complainVO)
            return render_template('user/viewComplainReply.html', complainVOList=complainVOList, userName=userName)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainList = complainDAO.userDeleteComplain(complainVO)

            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath.replace('..', 'project')

            path = complainFilePath + complainFileName

            if complainFileName != "None":
                os.remove(path)

            if complainList.complainStatus == 'Replied':
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath.replace('..', 'project')
                path = replyFilePath + replyFileName
                os.remove(path)

            return redirect(url_for('userViewComplain'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainStatus = 'Pending'
            complainVO.complainStatus = complainStatus

            complainVOList = complainDAO.adminViewComplain(complainVO)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplain():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplain():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER = 'project/static/adminResources/replyAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            file = request.files['replyFilename']
            print(file)

            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(replyFilePath)

            file.save(os.path.join(replyFilePath, replyFileName))

            complainTo_LoginId = session.get('session_loginId')
            complainStatus = 'Replied'
            replyDate = str(date.today())
            replyTime = str(datetime.now().strftime("%H:%M:%S"))

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainId = complainId
            complainVO.complainTo_LoginId = complainTo_LoginId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainStatus = complainStatus
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace('project', '..')

            complainDAO.insertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)
