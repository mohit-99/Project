from project import db
from project.com.vo.VideoVO import VideoVO


class RegionFourVO(db.Model):
    __tablename__ = 'regionfourmaster'
    regionFourId = db.Column('regionFourId', db.Integer, primary_key=True, autoincrement=True)
    regionFourPerson = db.Column('regionFourPerson', db.Integer)
    regionFourTime = db.Column('regionFourTime', db.Integer)
    regionFour_VideoId = db.Column('regionFour_VideoId', db.Integer, db.ForeignKey(VideoVO.videoId))


def as_dict(self):
    return {
        'regionFourId': self.regionFourId,
        'regionFourPerson': self.regionFourPerson,
        'regionFourTime': self.regionFourTime,
        'regionFour_VideoId': self.regionFour_VideoId
    }


db.create_all()
