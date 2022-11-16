from db import *
from ..user_info_function import UserInfo
import utils
import convSetting

# 单聊
def create_conv_private(uidList):
    uidList = sorted(uidList)   #  按uid大小排序
    try:
        user1 = UserInfo.query.filter(id = uidList[0]).one()
        user2 = UserInfo.query.filter(id = uidList[1]).one()
        if user1 is None or user2 is None:
            raise ValueError('Invalid user id!')
        if ConvInfo.query.filter_by(convLongId = utils.get_convLongId(uidList)).count() == 0:
            raise ValueError('Duplicate private conversation!')        
        convInfo = ConvInfo(
            conType = 1, 
            name = f'{user1.name}与{user2.name}的会话', 
            convLongId = utils.get_convLongId(uidList)
        )
        err, msg = convSetting.create_conv_settings(convInfo.id, uidList)
        if err != 0:
            raise Exception(msg)
        db.session.add(convInfo)
        db.session.commit()
        return 0, f'[Info] Create conversation successfully!'
    except Exception as e:
        db.session.rollback()
        return -1, f'[Error] {e} when creating conversation with {uidList}'

def get_conv_info(convId):
    try:
        convInfo = ConvInfo.query.filter(convId == convId).first()
        if convInfo is None:
            raise KeyError('Conversation not exist!')
        return 0, convInfo
    except Exception as e:
        return -1, f'[Error] {e} when getting info of {convId}!'