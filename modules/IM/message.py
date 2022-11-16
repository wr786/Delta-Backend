from db import *
from ..user_info_function import UserInfo
import utils

def send_message(sender, convId, content):
    try:
        user = UserInfo.query.filter(id=sender).one()
        if user is None:
            raise KeyError('User not exist!')
        conv = ConvInfo.query.filter(id=convId).one()
        if conv is None:
            raise KeyError('Conversation not exist!')
        
        message = Message(
            uid = sender,
            convId = convId,
            content = content
        )
        db.session.add(message)
        db.session.commit()
        return 0, f'[Info] Send message successfully!'
        # return后要根据convSetting通知会话中的其他成员
    except Exception as e:
        db.session.rollback()
        return -1, f'[Error] {e} when sending message with sender={sender}, convId={convId}'

def get_all_message(convId):
    try:
        conv = ConvInfo.query.filter(id=convId).one()
        if conv is None:
            raise KeyError('Conversation not exist!')

        allMsg = Message.query.filter_by(convId=convId).all().order_by(id.desc())
        return 0, allMsg
    except Exception as e:
        return -1, f'[Error] Get all message of {convId} failed: {e}'

def get_recent_message_by_conv(convId):
    try:
        conv = ConvInfo.query.filter(id=convId).one()
        if conv is None:
            raise KeyError('Conversation not exist!')

        recentMsg = Message.query.filter_by(convId=convId).order_by(id.desc()).limit(utils.RECENT_MESSAGE_COUNT)
        return 0, recentMsg
    except Exception as e:
        return -1, f'[Error] Get recent message of convId={convId} failed: {e}'

def get_recent_message_by_user(uid):
    # 需要每个群聊都有，不然会有消息挨饿
    try:
        user = UserInfo.query.filter(id=uid).one()
        if user is None:
            raise KeyError('User not exist!')

        recentMsg = []
        userConvIds = db.session.query(db.distinct(Message.convId)).filter_by(uid=uid).all()
        for userConvId in userConvIds:
            recentMsg.append(*Message.query.filter_by(uid=uid, convId=userConvId).order_by(id.desc()).limit(utils.RECENT_MESSAGE_COUNT))
        return 0, recentMsg            
    except Exception as e:
        return -1, f'[Error] Get recent message of uid={uid} failed: {e}'