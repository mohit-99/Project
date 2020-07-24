from sqlalchemy import func
from project import db
from project.com.vo.RegionTwoVO import RegionTwoVO
from project.com.vo.VideoVO import VideoVO


class RegionTwoDAO:
    def insertLogTwo(self, regionVO):
        db.session.add(regionVO)
        db.session.commit()

    def updateRegionTwo(self, regionVO):
        db.session.merge(regionVO)
        db.session.commit()

    def regionTwoPersonCount(self, regionVO):
        regionTwoList = db.session.query(func.sum(RegionTwoVO.regionTwoPerson).label("regionTwoPersonCount")). \
            filter_by(regionTwo_VideoId=regionVO.regionTwo_VideoId).first()
        return regionTwoList

    def regionTwoTimeCount(self, regionVO):
        regionTwoList = db.session.query(func.sum(RegionTwoVO.regionTwoTime).label("regionTwoTimeCount")). \
            filter_by(regionTwo_VideoId=regionVO.regionTwo_VideoId).first()
        return regionTwoList

    def findRegionTwoByVideoId(self, regionTwoVO):
        regionTwoList = RegionTwoVO.query.filter_by(regionTwo_VideoId=regionTwoVO.regionTwo_VideoId).all()
        return regionTwoList

    def deleteRegionTwo(self, regionTwoVO):
        regionTwoList = RegionTwoVO.query.get(regionTwoVO.regionTwoId)
        db.session.delete(regionTwoList)
        db.session.commit()