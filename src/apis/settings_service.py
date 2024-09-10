from esearch.index import ESearch
import psycopg2
from sqlalchemy.orm import Session

from src.database.schemas.setting_schema import SettingCreate, ShowSetting
import src.database.repository.setting as setting_repository
from src.utils import create_schema_json
from src.utils.index import generate_secret_key, generate_index_name
import src.helpers.response as response


def create_new_setting(setting: SettingCreate, db: Session):
    existing_setting = setting_repository.get_setting_by_email(setting.email, db)
    if existing_setting:
        return response.error_response('email already exists', 403)
    secret_key = generate_secret_key(20)

    es_index = generate_index_name(setting.db_name, setting.db_table)
    created_setting = setting_repository.create_new_setting(setting=setting, db=db, secret_key=secret_key,
                                                            es_index=es_index)

    create_schema_json.create_json_file(setting.db_name, setting.db_table, es_index, setting.columns)
    return created_setting


def get_total_rows(setting: SettingCreate):
    DATABASE_URL = f"dbname='{setting.db_name}' user='{setting.db_user}' host='{setting.db_host}' password='{setting.db_password}' port='{setting.db_port}'"
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {setting.db_table}")
        total_rows = cur.fetchone()[0]
        cur.close()
        return total_rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None and conn.closed == 0:
            conn.close()


def get_index_status(email: str, db: Session):
    existing_setting = setting_repository.get_setting_by_email(email, db)
    if not existing_setting:
        return response.error_response('setting does not exist', 404)
    es = ESearch()
    try:
        index_data = es.client.indices.stats(index=existing_setting.es_index)
    except Exception as e:
        return response.error_response(f' {e}', 404)
    index_count = index_data["indices"][existing_setting.es_index]["primaries"]["docs"]["count"]
    db_count = get_total_rows(existing_setting)
    completion_percentage = (index_count / db_count) * 100

    return response.success_response(
        {'db_count': db_count, 'es_count': index_count, "completion_percentage": completion_percentage})
