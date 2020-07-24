from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BranchVO import BranchVO
from project.com.vo.LoginVO import LoginVO


class VideoVO(db.Model):
    __tablename__ = 'videomaster'
    videoId = db.Column('videoId', db.Integer, primary_key=True, autoincrement=True)
    inputVideoFileName = db.Column('inputVideoFileName', db.String(100))
    inputVideoFilePath = db.Column('inputVideoFilePath', db.String(100))
    inputVideoUploadDate = db.Column('inputVideoUploadDate', db.String(100))
    inputVideoUploadTime = db.Column('inputVideoUploadTime', db.String(100))
    outputVideoFileName = db.Column('outputVideoFileName', db.String(100))
    outputVideoFilePath = db.Column('outputVideoFilePath', db.String(100))
    outputVideoUploadDate = db.Column('outputVideoUploadDate', db.String(100))
    outputVideoUploadTime = db.Column('outputVideoUploadTime', db.String(100))
    video_BranchId = db.Column('video_BranchId', db.Integer, db.ForeignKey(BranchVO.branchId))
    video_AreaId = db.Column('video_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    video_LoginId = db.Column('video_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'videoId': self.videoId,
            'inputVideoFileName': self.inputVideoFileName,
            'inputVideoFilePath': self.inputVideoFilePath,
            'inputVideoUploadDate': self.inputVideoUploadDate,
            'inputVideoUploadTime': self.inputVideoUploadTime,
            'outputVideoFileName': self.outputVideoFileName,
            'outputVideoFilePath': self.outputVideoFilePath,
            'outputVideoUploadDate': self.outputVideoUploadDate,
            'outputVideoUploadTime': self.outputVideoUploadTime,
            'video_BranchId': self.video_BranchId,
            'video_AreaId': self.video_AreaId,
            'video_LoginId': self.video_LoginId
        }


db.create_all()
