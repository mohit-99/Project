from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def validateLogin(self, LoginVO):
        loginList = LoginVO.query.filter_by(loginUsername=LoginVO.loginUsername,
                                            loginPassword=LoginVO.loginPassword).all()
        return loginList

    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()

        return loginList

    def loginUpdateUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()
