from project import db
from project.com.vo.BranchVO import BranchVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.RestaurantVO import RestaurantVO
from project.com.vo.LoginVO import LoginVO


class BranchDAO:
    def insertBranch(self, branchVO):
        db.session.add(branchVO)
        db.session.commit()

    def viewBranch(self, branchVO):
        branchList = db.session.query(BranchVO, AreaVO) \
            .filter_by(branch_RestaurantId=branchVO.branch_RestaurantId) \
            .join(AreaVO, BranchVO.branch_AreaId == AreaVO.areaId).all()
        return branchList

    def adminViewBranch(self):
        branchList = db.session.query(BranchVO, AreaVO) \
            .join(AreaVO, BranchVO.branch_AreaId == AreaVO.areaId).all()
        return branchList

    def deleteBranch(self, branchVO):
        branchList = BranchVO.query.get(branchVO.branchId)

        db.session.delete(branchList)

        db.session.commit()

    def editBranch(self, branchVO):
        branchList = BranchVO.query.filter_by(branchId=branchVO.branchId).all()
        return branchList

    def updateBranch(self, branchVO):
        db.session.merge(branchVO)

        db.session.commit()

    def getAreaByBranch(self, branchVO):
        branchList = BranchVO.query.filter_by(branchId=branchVO.branchId).all()
        return branchList
