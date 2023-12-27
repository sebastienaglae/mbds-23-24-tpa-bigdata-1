import json
import nats
import nats.js
import asyncio
import sqlite3
import hashlib

class Databus:
    nc = nats.NATS
    js = nats.js.JetStreamContext

    def __init__(self, conf):
        self.nc_host = conf["host"]
        self.max_concurrent = conf["max_concurrent"]
        self.pub_subject = conf["pub_subject"]
        self.mode_subject_map = conf["mode_subject_map"]
        self.enable_sqlite = conf["enable_smart_upsert"]
        if self.enable_sqlite:
            self.sqlite_conn = sqlite3.connect(conf["sqlite_db_path"])
            self.sqlite_cursor = self.sqlite_conn.cursor()

    async def connect(self):
        self.nc = await nats.connect(self.nc_host)
        self.js = self.nc.jetstream()

    async def publish_result(self, collection_name, collected_data, pk_attrs, transformer, mode: str = "upsert"):
        if not mode in self.mode_subject_map:
            raise Exception("Unknown mode subject translation: " + mode)

        if self.enable_sqlite:
            self.sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS " + collection_name + " (id TEXT PRIMARY KEY, hash TEXT)")
        
        pk_attrs_str = pk_attrs if isinstance(pk_attrs, str) else ",".join(pk_attrs)
        pub_subject = self.pub_subject.replace("<type>", collection_name).replace("<mode>", mode)
        running_tasks = []
        for row_data in collected_data:
            transformed_data = transformer(row_data)
            json_data = json.dumps(transformed_data)
            json_data_bytes = bytes(json_data, "utf-8")
            if self.enable_sqlite:
                hash = hashlib.sha256(json_data_bytes).hexdigest()
                key_value = transformed_data[pk_attrs] if isinstance(pk_attrs, str) else ",".join([str(transformed_data[attr]) for attr in pk_attrs])
                current_hash = self.sqlite_cursor.execute("SELECT hash FROM " + collection_name + " WHERE id = ?", (key_value,)).fetchone()
                if current_hash is None:
                    self.sqlite_cursor.execute("INSERT INTO " + collection_name + " VALUES (?, ?)", (key_value, hash))
                elif current_hash[0] != hash:
                    self.sqlite_cursor.execute("UPDATE " + collection_name + " SET hash = ? WHERE id = ?", (hash, key_value))
                else:
                    continue
            running_tasks.append(self.js.publish(pub_subject, json_data_bytes, headers={"table": collection_name, "tablePk": pk_attrs_str}))
            if len(running_tasks) == self.max_concurrent:
                await asyncio.gather(*running_tasks)
                running_tasks = []
        if len(running_tasks) > 0:
            await asyncio.gather(*running_tasks)
        if self.enable_sqlite:
            self.sqlite_conn.commit()
