from project import db
from project.com.vo.FeedbackVO import FeedbackVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def viewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()
        return feedbackList

    def adminViewFeedback(self):
        feedbackList = FeedbackVO.query.all()
        return feedbackList

    def updateFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()

    def deleteFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.get(feedbackVO.feedbackId)
        db.session.delete(feedbackList)
        db.session.commit()
