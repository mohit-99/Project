from project import db
from project.com.vo.VideoVO import VideoVO
from project.com.vo.RegionOneVO import RegionOneVO
from sqlalchemy import func


class RegionOneDAO:
    def insertLogOne(self, regionVO):
        db.session.add(regionVO)
        db.session.commit()

    def updateRegionOne(self, regionVO):
        db.session.merge(regionVO)
        db.session.commit()

    def regionOnePersonCount(self, regionVO):
        regionOneList = db.session.query(func.sum(RegionOneVO.regionOnePerson).label("regionOnePersonCount")). \
            filter_by(regionOne_VideoId=regionVO.regionOne_VideoId).first()
        return regionOneList

    def regionOneTimeCount(self, regionVO):
        regionOneList = db.session.query(func.sum(RegionOneVO.regionOneTime).label("regionOneTimeCount")). \
            filter_by(regionOne_VideoId=regionVO.regionOne_VideoId).first()
        return regionOneList

    def findRegionOneByVideoId(self, regionOneVO):
        regionOneList = RegionOneVO.query.filter_by(regionOne_VideoId=regionOneVO.regionOne_VideoId).all()
        return regionOneList

    def deleteRegionOne(self, regionOneVO):
        regionOneList = RegionOneVO.query.get(regionOneVO.regionOneId)
        db.session.delete(regionOneList)
        db.session.commit()