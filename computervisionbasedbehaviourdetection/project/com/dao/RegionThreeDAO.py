from project import db
from project.com.vo.RegionThreeVO import RegionThreeVO
from project.com.vo.VideoVO import VideoVO
from sqlalchemy import func


class RegionThreeDAO:
    def insertLogThree(self, regionVO):
        db.session.add(regionVO)
        db.session.commit()

    def updateRegionThree(self, regionVO):
        db.session.merge(regionVO)
        db.session.commit()

    def regionThreePersonCount(self, regionVO):
        regionThreeList = db.session.query(func.sum(RegionThreeVO.regionThreePerson).label("regionThreePersonCount")). \
            filter_by(regionThree_VideoId=regionVO.regionThree_VideoId).first()
        return regionThreeList

    def regionThreeTimeCount(self, regionVO):
        regionThreeList = db.session.query(func.sum(RegionThreeVO.regionThreeTime).label("regionThreeTimeCount")). \
            filter_by(regionThree_VideoId=regionVO.regionThree_VideoId).first()
        return regionThreeList

    def findRegionThreeByVideoId(self, regionThreeVO):
        regionThreeList = RegionThreeVO.query.filter_by(regionThree_VideoId=regionThreeVO.regionThree_VideoId).all()
        return regionThreeList

    def deleteRegionThree(self, regionThreeVO):
        regionThreeList = RegionThreeVO.query.get(regionThreeVO.regionThreeId)
        db.session.delete(regionThreeList)
        db.session.commit()