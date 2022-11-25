from ..sendemail import cache

def check_captcha(email,captcha):
    cap=cache.get(email)
    if cap==captcha:
        return True
    return False