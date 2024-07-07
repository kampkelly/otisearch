from sqlalchemy.orm import Session

from src.database.schemas.setting import SettingCreate
from src.database.models.setting import Setting


def create_new_setting(setting: SettingCreate, db: Session, secret_key: str, es_index: str):
    setting = Setting(
        email=setting.email,
        secret_key=secret_key,
        db_user=setting.db_user,
        db_name=setting.db_name,
        db_host=setting.db_host,
        db_password=setting.db_password,
        db_port=setting.db_port,
        db_table=setting.db_table,
        db_schema=setting.db_schema,
        es_index=es_index
    )
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def get_setting_by_email(email: str, db: Session):
    setting = db.query(Setting).filter(Setting.email == email).first()
    return setting
