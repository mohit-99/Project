from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.RestaurantVO import RestaurantVO


class BranchVO(db.Model):
    __tablename__ = 'branchmaster'
    branchId = db.Column('branchId', db.Integer, primary_key=True, autoincrement=True)
    branchCode = db.Column('branchCode', db.Integer)
    branchName = db.Column('branchName', db.String(100))
    branch_AreaId = db.Column('branch_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    branch_RestaurantId = db.Column('branch_RestaurantId', db.Integer, db.ForeignKey(RestaurantVO.restaurantId))

    def as_dict(self):
        return {
            'branchId': self.branchId,
            'branchCode': self.branchCode,
            'branchName': self.branchName,
            'branch_AreaId': self.branch_AreaId,
            'branch_RestaurantId': self.branch_RestaurantId
        }


db.create_all()
