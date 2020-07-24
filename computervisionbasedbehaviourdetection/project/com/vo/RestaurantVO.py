from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.AreaVO import AreaVO


class RestaurantVO(db.Model):
    __tablename__ = 'restaurantmaster'
    restaurantId = db.Column('restaurantId', db.Integer, primary_key=True, autoincrement=True)
    restaurantName = db.Column('restaurantName', db.String(100), nullable=False)
    restaurantNumber = db.Column('restaurantNumber', db.Numeric, nullable=False)
    restaurantOwner = db.Column('restaurantOwner', db.String(100), nullable=False)
    restaurant_AreaId = db.Column('restaurant_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    restaurant_LoginId = db.Column('restaurant_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'restaurantId': self.restaurantId,
            'restaurantName': self.restaurantName,
            'restaurantNumber': self.restaurantNumber,
            'restaurantOwner': self.restaurantOwner,
            'restaurant_AreaId': self.restaurant_AreaId,
            'restaurant_LoginId': self.restaurant_LoginId
        }


db.create_all()
