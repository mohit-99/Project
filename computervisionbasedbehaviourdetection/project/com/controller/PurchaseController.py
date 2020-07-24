from flask import request, render_template, redirect, url_for, session
from datetime import datetime, date

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.dao.PackageDAO import PackageDAO


@app.route('/user/loadPurchase', methods=['GET'])
def userLoadPackage():
    try:
        if adminLoginSession() == 'user':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            return render_template('user/addPurchase.html', packageVOList=packageVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertPurchase', methods=['GET'])
def userInsertPurchase():
    try:
        if adminLoginSession() == 'user':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()

            purchase_LoginId = session.get('session_loginId')
            purchaseVO.purchase_LoginId = purchase_LoginId
            purchaseVOList = purchaseDAO.viewPurchase(purchaseVO)

            if len(purchaseVOList) == 0:

                purchase_LoginId = session.get('session_loginId')
                purchase_PackageId = request.args.get('packageId')

                purchaseDate = str(date.today())
                purchaseTime = str(datetime.now().strftime("%H:%M:%S"))

                purchaseVO.purchaseDate = purchaseDate
                purchaseVO.purchaseTime = purchaseTime
                purchaseVO.purchase_LoginId = purchase_LoginId
                purchaseVO.purchase_PackageId = purchase_PackageId

                purchaseDAO.insertPurchase(purchaseVO)

                return redirect(url_for('userViewPurchase'))
            else:
                return redirect(url_for('userViewPurchase'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/loadPayment', methods=['GET'])
def userLoadPayment():
    try:
        if adminLoginSession() == 'user':
            packageId = request.args.get('packageId')
            return render_template('user/addPayment.html', packageId=packageId)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertPaymentDetails', methods=['POST', 'GET'])
def userInsertPaymentDetails():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()
            packageId = request.args.get('packageId')
            cardName = request.form['cardName']
            cvv = request.form['cvv']
            cardNumber = request.form['cardNumber']
            expirationMonth = request.form['expiration-month']
            expirationYear = request.form['expiration-year']
            expirationDate = expirationMonth + "/" + expirationYear
            print(len(cardName))
            if len(cardName) == 0:
                msg = "Enter Owner Name"
                return render_template('user/addPayment.html', error=msg)
            elif len(cvv) < 3:
                msg = "Enter CVV "
                return render_template('user/addPayment.html', error=msg)
            elif len(cardNumber) < 19:
                msg = "Enter a valid Card Number "
                return render_template('user/addPayment.html', error=msg)
            elif len(expirationDate) == 0:
                msg = "Select an expiration date "
                return render_template('user/addPayment.html', error=msg)
            else:
                return redirect(url_for('userInsertPurchase'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/viewPurchase', methods=['GET'])
def userViewPurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchase_LoginId = session.get('session_loginId')

            purchaseVO.purchase_LoginId = purchase_LoginId

            purchaseVOList = purchaseDAO.viewPurchase(purchaseVO)

            return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deletePurchase', methods=['GET'])
def userDeletePurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchaseId = request.args.get('purchaseId')
            purchaseVO.purchaseId = purchaseId

            purchaseDAO.deletePurchase(purchaseVO)

            return redirect(url_for('userViewPurchase'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
