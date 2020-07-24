from project import db
from project.com.vo.VideoVO import VideoVO


class RegionTwoVO(db.Model):
    __tablename__ = 'regiontwomaster'
    regionTwoId = db.Column('regionTwoId', db.Integer, primary_key=True, autoincrement=True)
    regionTwoPerson = db.Column('regionTwoPerson', db.Integer)
    regionTwoTime = db.Column('regionTwoTime', db.Integer)
    regionTwo_VideoId = db.Column('regionTwo_VideoId', db.Integer, db.ForeignKey(VideoVO.videoId))


def as_dict(self):
    return {
        'regionTwoId': self.regionTwoId,
        'regionTwoPerson': self.regionTwoPerson,
        'regionTwoTime': self.regionTwoTime,
        'regionTwo_VideoId': self.regionTwo_VideoId
    }


db.create_all()
