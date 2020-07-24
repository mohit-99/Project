import os
from datetime import datetime, date

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

UPLOAD_DATASET_FOLDER = 'project/static/adminResources/dataset/'
app.config['UPLOAD_FOLDER'] = UPLOAD_DATASET_FOLDER


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['file']
            print(file)

            datasetFileName = secure_filename(file.filename)
            print(datasetFileName)

            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(datasetFilePath)

            datasetUploadDate = str(date.today())
            print(datasetUploadDate)

            datasetUploadTime = str(datetime.now().strftime("%H:%M:%S"))
            print(datasetUploadTime)

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetVO.datasetFileName = datasetFileName
            datasetVO.datasetFilePath = datasetFilePath.replace('project', '..')
            datasetVO.datasetUploadDate = datasetUploadDate
            datasetVO.datasetUploadTime = datasetUploadTime

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()

            return render_template('admin/viewDataset.html', datsetVOList=datasetVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')

            datasetVO.datasetId = datasetId

            datasetList = datasetDAO.deleteDataset(datasetVO)

            print(datasetList)

            datasetFilename = datasetList.datasetFileName
            datasetFilepath = datasetList.datasetFilePath.replace('..', 'project')

            path = datasetFilepath + datasetFilename

            os.remove(path)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
