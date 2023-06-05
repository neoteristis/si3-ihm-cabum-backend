from firebase_admin import messaging

def sendNotification(app, title:str, msg:str, fcm:str):
    msg=messaging.Notification(title=title, body=msg)
    fmsg=messaging.Message(notification=msg,token=fcm)
    messaging.send(message=fmsg,app=app)