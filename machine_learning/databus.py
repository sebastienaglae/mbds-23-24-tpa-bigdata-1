import json
import nats
import nats.js
import asyncio

class Databus:
    nc = nats.NATS
    js = nats.js.JetStreamContext

    def __init__(self, conf):
        self.nc_host = conf["host"]
        self.max_concurrent = conf["max_concurrent"]
        self.pub_subject = conf["pub_subject"]
        self.mode_subject_map = conf["mode_subject_map"]

    async def connect(self):
        self.nc = await nats.connect(self.nc_host)
        self.js = self.nc.jetstream()

    async def publish_result(self, collection_name, collected_data, pk_attrs, transformer, mode: str = "upsert"):
        if not mode in self.mode_subject_map:
            raise Exception("Unknown mode subject translation: " + mode)

        pk_attrs_str = pk_attrs if isinstance(pk_attrs, str) else ",".join(pk_attrs)
        pub_subject = self.pub_subject.replace("<type>", collection_name).replace("<mode>", mode)
        running_tasks = []
        for row_data in collected_data:
            transformed_data = transformer(row_data)
            json_data = json.dumps(transformed_data)
            json_data_bytes = bytes(json_data, "utf-8")
            running_tasks.append(self.js.publish(pub_subject, json_data_bytes, headers={"table": collection_name, "tablePk": pk_attrs_str}))
            if len(running_tasks) == self.max_concurrent:
                await asyncio.gather(*running_tasks)
                running_tasks = []
        if len(running_tasks) > 0:
            await asyncio.gather(*running_tasks)
