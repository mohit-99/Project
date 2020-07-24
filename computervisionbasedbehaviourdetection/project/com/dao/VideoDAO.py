from project import db
from project.com.vo.VideoVO import VideoVO
from project.com.vo.RestaurantVO import RestaurantVO
from project.com.vo.BranchVO import BranchVO


class VideoDAO:
    def insertVideo(self, videoVO):
        db.session.add(videoVO)
        db.session.commit()

    def viewVideo(self, videoVO):
        videoList = VideoVO.query.filter_by(video_LoginId=videoVO.video_LoginId).all()
        return videoList

    def viewVideoByArea(self, videoVO):
        videoList = VideoVO.query.filter_by(video_LoginId=videoVO.video_LoginId,
                                            video_AreaId=videoVO.video_AreaId).all()
        return videoList

    def deleteVideo(self, videoVO):
        videoList = VideoVO.query.get(videoVO.videoId)
        db.session.delete(videoList)
        db.session.commit()
        return videoList

    def adminViewVideo(self):
        videoList = db.session.query(VideoVO, BranchVO, RestaurantVO) \
            .join(BranchVO, VideoVO.video_BranchId == BranchVO.branchId) \
            .join(RestaurantVO, BranchVO.branch_RestaurantId == RestaurantVO.restaurantId) \
            .all()
        return videoList

    def insertLog(self, regionVO):
        db.session.add(regionVO)
        db.session.commit()

    def viewVideoByBranch(self, videoVO):
        videoList = VideoVO.query.filter_by(video_BranchId=videoVO.video_BranchId).all()
        return videoList
