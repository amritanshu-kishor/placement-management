from contextlib import contextmanager
from pathlib import Path

import pymysql.err

ROOT = Path(__file__).resolve().parent

# Host must be a DNS name or IP (e.g. localhost, 127.0.0.1, db.example.com).
# Do not use a MySQL Workbench "connection name" here — that is only a label in the UI.
DB_HOST = "127.0.0.1"
DB_USER = "dhiraj"
DB_PASSWORD = "dhiraj@2006"
DB_NAME = "placement"


def _raw_connect():
    return pymysql.connect(
        host=str(DB_HOST).strip(),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


class _CursorResult:
    def __init__(self, cursor):
        self._cursor = cursor

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    @property
    def lastrowid(self):
        return self._cursor.lastrowid


class Conn:
    def __init__(self, raw):
        self._raw = raw

    def execute(self, sql, args=None):
        cur = self._raw.cursor()
        cur.execute(sql, args or ())
        return _CursorResult(cur)


@contextmanager
def get_db():
    raw = _raw_connect()
    conn = Conn(raw)
    try:
        yield conn
        raw.commit()
    except Exception:
        raw.rollback()
        raise
    finally:
        raw.close()


def init_db(schema_path=None):
    path = Path(schema_path) if schema_path else ROOT / "schema.sql"
    sql_text = path.read_text(encoding="utf-8")
    raw = _raw_connect()
    try:
        for part in sql_text.split(";"):
            stmt = part.strip()
            if stmt:
                with raw.cursor() as cur:
                    try:
                        cur.execute(stmt)
                    except pymysql.err.OperationalError as e:
                        # 1061 = duplicate key name (re-run of schema.sql)
                        if e.args[0] == 1061:
                            continue
                        raise
        raw.commit()
    finally:
        raw.close()


if __name__ == "__main__":
    init_db()
    print("Tables ensured from schema.sql")
