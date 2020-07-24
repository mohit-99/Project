from sqlalchemy import func

from project import db
from project.com.vo.RegionFourVO import RegionFourVO
from project.com.vo.VideoVO import VideoVO


class RegionFourDAO:
    def insertLogFour(self, regionVO):
        db.session.add(regionVO)
        db.session.commit()

    def updateRegionFour(self, regionVO):
        db.session.merge(regionVO)
        db.session.commit()

    def regionFourPersonCount(self, regionVO):
        regionFourList = db.session.query(func.sum(RegionFourVO.regionFourPerson).label("regionFourPersonCount")). \
            filter_by(regionFour_VideoId=regionVO.regionFour_VideoId).first()
        return regionFourList

    def regionFourTimeCount(self, regionVO):
        regionFourList = db.session.query(func.sum(RegionFourVO.regionFourTime).label("regionFourTimeCount")). \
            filter_by(regionFour_VideoId=regionVO.regionFour_VideoId).first()
        return regionFourList
    
    def findRegionFourByVideoId(self, regionFourVO):
        regionFourList = RegionFourVO.query.filter_by(regionFour_VideoId=regionFourVO.regionFour_VideoId).all()
        return regionFourList

    def deleteRegionFour(self, regionFourVO):
        regionFourList = RegionFourVO.query.get(regionFourVO.regionFourId)
        db.session.delete(regionFourList)
        db.session.commit()
