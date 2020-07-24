from project import db
from project.com.vo.RestaurantVO import RestaurantVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.LoginVO import LoginVO


class RestaurantDAO:
    def insertRestaurant(self, restaurantVO):
        db.session.add(restaurantVO)
        db.session.commit()

    def viewUser(self):
        userList = db.session.query(RestaurantVO, LoginVO, AreaVO) \
            .join(AreaVO, RestaurantVO.restaurant_AreaId == AreaVO.areaId) \
            .join(LoginVO, RestaurantVO.restaurant_LoginId == LoginVO.loginId) \
            .all()
        return userList

    def viewRestaurant(self, restaurantVO):
        restaurantList = RestaurantVO.query.filter_by(restaurant_LoginId=restaurantVO.restaurant_LoginId).all()
        return restaurantList
