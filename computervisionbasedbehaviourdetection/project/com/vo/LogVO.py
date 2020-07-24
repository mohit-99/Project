from project import db
from project.com.vo.VideoVO import VideoVO
from project.com.vo.LoginVO import LoginVO


class LogVO(db.Model):
    __tablename__ = 'logmaster'
    logId = db.Column('logId', db.Integer, primary_key=True, autoincrement=True)
    region1Person = db.Column('region1Person', db.Integer)
    region1Time = db.Column('region1Time', db.Integer)
    region2Person = db.Column('region2Person', db.Integer)
    region2Time = db.Column('region2Time', db.Integer)
    region3Person = db.Column('region3Person', db.Integer)
    region3Time = db.Column('region3Time', db.Integer)
    region4Person = db.Column('region4Person', db.Integer)
    region4Time = db.Column('region4Time', db.Integer)
    log_LoginId = db.Column('log_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'logId': self.logId,
            'region1Person': self.region1Person,
            'region1Time': self.region1Time,
            'region2Person': self.region2Person,
            'region2Time': self.region2Time,
            'region3Person': self.region3Person,
            'region3Time': self.region3Time,
            'region4Person': self.region4Person,
            'region4Time': self.region4Time,
            'log_LoginId': self.log_LoginId
        }


db.create_all()
