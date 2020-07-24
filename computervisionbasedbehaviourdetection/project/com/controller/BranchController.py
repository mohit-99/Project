from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.BranchDAO import BranchDAO
from project.com.vo.BranchVO import BranchVO
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.RestaurantDAO import RestaurantDAO
from project.com.vo.RestaurantVO import RestaurantVO


@app.route('/user/loadBranch', methods=['GET'])
def userLoadBranch():
    try:
        if adminLoginSession() == 'user':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            return render_template('user/addBranch.html', areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertBranch', methods=['POST'])
def userInsertBranch():
    try:
        if adminLoginSession() == 'user':
            branchName = request.form['branchName']
            branchCode = request.form['branchCode']
            branch_AreaId = request.form['branch_AreaId']
            restaurant_loginId = session['session_loginId']

            restaurantDAO = RestaurantDAO()
            restaurantVO = RestaurantVO()

            restaurantVO.restaurant_LoginId = restaurant_loginId
            restaurantVOList = restaurantDAO.viewRestaurant(restaurantVO)
            print(restaurantVOList)

            branchVO = BranchVO()
            branchDAO = BranchDAO()

            branchVO.branchName = branchName
            branchVO.branchCode = branchCode
            branchVO.branch_AreaId = branch_AreaId
            branchVO.branch_RestaurantId = restaurantVOList[0].restaurantId
            branchDAO.insertBranch(branchVO)

            return redirect(url_for('userViewBranch'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewBranch', methods=['GET'])
def userViewBranch():
    try:
        if adminLoginSession() == 'user':
            branchDAO = BranchDAO()
            branchVO = BranchVO()
            restaurantDAO = RestaurantDAO()
            restaurantVO = RestaurantVO()

            restaurant_loginId = session['session_loginId']

            restaurantVO.restaurant_LoginId = restaurant_loginId
            restaurantVOList = restaurantDAO.viewRestaurant(restaurantVO)
            branchVO.branch_RestaurantId = restaurantVOList[0].restaurantId

            branchVOList = branchDAO.viewBranch(branchVO)

            return render_template('user/viewBranch.html', branchVOList=branchVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteBranch', methods=['GET'])
def userDeleteBranch():
    try:
        if adminLoginSession() == 'user':
            branchVO = BranchVO()

            branchDAO = BranchDAO()

            branchId = request.args.get('branchId')

            branchVO.branchId = branchId

            branchDAO.deleteBranch(branchVO)

            return redirect(url_for('userViewBranch'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/editBranch', methods=['GET'])
def userEditBranch():
    try:
        if adminLoginSession() == 'user':
            branchVO = BranchVO()
            areaDAO = AreaDAO()
            branchDAO = BranchDAO()

            branchId = request.args.get('branchId')

            branchVO.branchId = branchId

            branchVOList = branchDAO.editBranch(branchVO)
            areaVOList = areaDAO.viewArea()
            # print("=======categoryVOList=======", categoryVOList)
            #
            # print("=======type of categoryVOList=======", type(categoryVOList))

            return render_template('user/editBranch.html', branchVOList=branchVOList, areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/updateBranch', methods=['POST'])
def userUpdateBranch():
    try:
        if adminLoginSession() == 'user':
            branchId = request.form['branchId']
            branchName = request.form['branchName']
            branchCode = request.form['branchCode']
            branch_AreaId = request.form['branch_AreaId']

            branchVO = BranchVO()
            branchDAO = BranchDAO()

            branchVO.branchId = branchId
            branchVO.branchName = branchName
            branchVO.branchCode = branchCode
            branchVO.branch_AreaId = branch_AreaId

            branchDAO.updateBranch(branchVO)

            return redirect(url_for('userViewBranch'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewBranch', methods=['GET'])
def adminViewBranch():
    try:
        if adminLoginSession() == 'admin':
            branchDAO = BranchDAO()
            branchVOList = branchDAO.adminViewBranch()

            return render_template('admin/viewBranch.html', branchVOList=branchVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
