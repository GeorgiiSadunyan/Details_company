import psycopg2

params = {
    "host": "localhost",
    "database": "Details_company",
    "user": "postgres",
    "password": "2121",
    "port": 5432,
}


class SupplierDBConnection:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.conn_params = params
            self.conn = psycopg2.connect(**self.conn_params)
            self.conn.autocommit = True
            self._initialized = True
            print("[INFO] Start connection")

    def _execute_query(self, query: str, params: tuple = ()) -> list[tuple]:
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def _execute_update(self, query: str, params: tuple = ()):
        with self.conn.cursor() as cur:
            cur.execute(query, params)

    def _close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("[INFO] Connection is closed")
        elif self.conn:
            print("[INFO] Connection was already closed")
