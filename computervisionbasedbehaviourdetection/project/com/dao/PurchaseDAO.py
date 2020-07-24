from project import db
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.vo.PackageVO import PackageVO
from project.com.vo.LoginVO import LoginVO


class PurchaseDAO:
    def insertPurchase(self, purchaseVO):
        db.session.add(purchaseVO)
        db.session.commit()

    def viewPurchase(self, purchaseVO):
        purchaseList = db.session.query(PurchaseVO, PackageVO, LoginVO).filter_by(
            purchase_LoginId=purchaseVO.purchase_LoginId). \
            join(PackageVO, PurchaseVO.purchase_PackageId == PackageVO.packageId). \
            join(LoginVO, PurchaseVO.purchase_LoginId == LoginVO.loginId).all()
        return purchaseList

    def deletePurchase(self, purchaseVO):
        purchaseList = PurchaseVO.query.get(purchaseVO.purchaseId)
        db.session.delete(purchaseList)
        db.session.commit()

    def validatePurchase(self, purchaseVO):
        purchaseList = PurchaseVO.query.filter_by(purchase_LoginId=purchaseVO.purchase_LoginId).all()
        return purchaseList
