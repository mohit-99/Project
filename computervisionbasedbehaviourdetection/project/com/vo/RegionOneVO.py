from project import db
from project.com.vo.VideoVO import VideoVO


class RegionOneVO(db.Model):
    __tablename__ = 'regiononemaster'
    regionOneId = db.Column('regionOneId', db.Integer, primary_key=True, autoincrement=True)
    regionOnePerson = db.Column('regionOnePerson', db.Integer)
    regionOneTime = db.Column('regionOneTime', db.Integer)
    regionOne_VideoId = db.Column('regionOne_VideoId', db.Integer, db.ForeignKey(VideoVO.videoId))


def as_dict(self):
    return {
        'regionOneId': self.regionOneId,
        'regionOnePerson': self.regionOnePerson,
        'regionOneTime': self.regionOneTime,
        'regionOne_VideoId': self.regionOne_VideoId
    }


db.create_all()
