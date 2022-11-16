from db import *
from ..user_info_function import UserInfo

def create_conv_settings(convId, uidList):
    try:
        for uid in uidList:
            convSetting = ConvSetting(
                uid=uid,
                convId=convId,
            )
            db.session.add(convSetting)
        db.session.commit()
        return 0, f'[Info] Create convSetting successfully!'
    except Exception as e:
        db.session.rollback()
        return -1, f'[Error] {e} when creating conversationSettings with convId={convId}, uidList={uidList}'