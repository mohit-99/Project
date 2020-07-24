from project import db
from project.com.vo.VideoVO import VideoVO


class RegionThreeVO(db.Model):
    __tablename__ = 'regionthreemaster'
    regionThreeId = db.Column('regionThreeId', db.Integer, primary_key=True, autoincrement=True)
    regionThreePerson = db.Column('regionThreePerson', db.Integer)
    regionThreeTime = db.Column('regionThreeTime', db.Integer)
    regionThree_VideoId = db.Column('regionThree_VideoId', db.Integer, db.ForeignKey(VideoVO.videoId))


def as_dict(self):
    return {
        'regionThreeId': self.regionThreeId,
        'regionThreePerson': self.regionThreePerson,
        'regionThreeTime': self.regionThreeTime,
        'regionThree_VideoId': self.regionThree_VideoId
    }


db.create_all()
