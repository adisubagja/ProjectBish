from userbot.modules.sql_helper import SESSION, BASE
from sqlalchemy import Column, String


class GoogleDriveCreds(BASE):
    __tablename__ = 'creds'
    user = Column(String(9), primary_key=True)
    credentials = Column(String(984), nullable=False)

    def __init__(self, user):
        self.user = user


GoogleDriveCreds.__table__.create(checkfirst=True)


def save_credentials(user, credentials):
    saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
    if not saved_credentials:
        saved_credentials = GoogleDriveCreds(user)

    saved_credentials.credentials = credentials

    SESSION.add(saved_credentials)
    SESSION.commit()
    return True


def get_credentials(user):
    try:
        saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
        creds = None

        if saved_credentials is not None:
            creds = saved_credentials.credentials
        return creds
    finally:
        SESSION.close()


def clear_credentials(user):
    saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
    if saved_credentials:
        SESSION.delete(saved_credentials)
        SESSION.commit()
        return True
