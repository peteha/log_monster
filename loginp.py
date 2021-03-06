import sys
import os
import json
import asyncio
import aiohttp
import uuid
import socket
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Initialize connection pool
conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
msg_pp = 50
tot_dblks = 10000
PARALLEL_REQUESTS = 100
sess_uuid = uuid.uuid4()
hostname = socket.gethostname()
results = []
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
testdata = "This is a test"
imagedata = "FYFWUng9ug+uRVhk2v8AvSeegHXIqJQrqoYbcZ+tVGPclysREZcjsp4Ipyk4DcYxj3qdU3JtIGRnHtU/2deuQrHqDVKmZubK/J2qeBjk+/bFKIQT8x46dKvrGWOc4B7j1pwjcDywOnt/StY0xOZT8rs3HHWpER9hZuM8H1z+VXPKViGYH1xzTvJbALdO/p+Va+yM3UKogwwZTjjjFWFjYjDD5kPIqZYsDJ9R9c1N5LKm1Oc8kmrjTJcypHGB9wkgHpnvUxiG4KDkjrxVv7O5yx6cVPFbfw56euKt0zJzM/yhs3KOc9aQxZbeQSR/nrWusOBlMnoKFi24RlyM/lTjTJdQzWjP+s5YdMVNuXOR3wen9avLbRnAQYGenrTjGqBe7YwMdqt0w9oZvlLu4H071J5UQY5HXqKuNCoAGePX07frUi26lipGSOme9CpCdRmc8O0Eg8+g4qSO2CjgnBJ98Vf8le/PPIA9aPs5P7pzyOav2fYiUyj5Lx88kD06intAAM43HjH/ANeroi2MDI2QegJ/pUxX5AGXoent9aSpi9oZRg2nB6fjUkcSKxPQN2NaHlKDgj147gVIICg3jn1NVyIOczUjlJOB29M4p5RkcSKOc8gjvV5oWwGYdqXyHPJGSvNJUxOoVPKIyOd3qKjMcmfmzj/PpWoY8AAjHHXn/wCvUhjZ1yN3KnjtT9mCmjGaEFvkxjqM/wCNOit/MY7M+g/+vWkYCWBQDP0ycUogySu0En8/zFNUw50UPs+xeO/BFNNuF6nnGMdua0o0eP5G6LjIoeHy23j+LoRS9kJzMsINmcZ9Se/509AUZnA64xV14RIxAXJH86mWD5chMgHnHFX7In2hmlR0/D15/GmCJWBIPPHHatVoIs/XnB79qUqDgFcEnP0Ao9kHtDOaFegXAP8AT0pTG6fe5PTHetEQqY9oI/HvTjB5mR0OeDVqmP2hnouDlRgdPpTxAjIF6luSO1aJhZF45PWpfJ+QMg7/AOfwqXTF7Qy1VUb92Mg9c08RoGORnd3Nay2+1gSAQenXNTC3z8p4UjoKapsTqmMsGfvZznP4U+K23nHTAwTW0bZVdSOceh6ipFtZAMp07fQ9DVxomfOjJ+x5Q5+bjscYpTbhl24PTvWyLEgjbnnjOan+zNu5UnscVapeQnURzptmEZDLyDycf41IIcNv28cdcf49s1vLZLhmZSFHc+tPW1AHzjrx0rT2BDqowhaBuCOuenFRrbs5+7jI4/yK6Q2eE5PH880Na9EHD9fwFP2AlXRzZtivzEYJHHHpThFxnGT9O9dK1sAQJOnvzUP2Rip3AfUUexH7ZGCbZlcSEHP+HpURth3Hc9fU1vm2lBwAB2/SpY7M+Z8x6c/nT9h5A6pzRhIRSnIJ49vX/wDXQ8UXAByT1z2rfktgpBQcEdO9R/ZCwVcdQOTj9al0UUqqOd8gZ3HHA6c/rTWtgpGBkexAJrpzZdepAPp29aiezHDNxxisnSKVY502wJB2nB5/X8KrmFUbjAI545+ldL9nkTLhScH/APVUMkDnhsAfdHfms3Rexr7U57ytoPJCt6dc0zy1bIYDqe3atiSEDIYDt+IFQiIN8hA9Af8AIqPYgqhjtGTz0IPPFU2iGflHp0/mK6BoWC5U9Dz7"
url = f'https://lic.pggb.net:9543/api/v1/events/ingest/{sess_uuid}'
db_1 = [{"events": [{"fields": [{"name": "hostname", "content": {hostname}}, {
    "name": "message_type", "content": "image"}, {
    "name": "seq_num", "content": i}], "text": imagedata + '/' + str(i)}for i in range(msg_pp)]} for j in range(tot_dblks)]
p = json.dumps(db_1, default=list)
pl = json.loads(p)
# for x in pl:
#    print(x['blk_num'])
#    del x['blk_num']
#    x = requests.post(url, json = x, verify=False)
#    print(x.text)
# print(pl)


async def gather_with_concurrency(n):
    semaphore = asyncio.Semaphore(n)
    session = aiohttp.ClientSession(connector=conn)

    # heres the logic for the generator
    async def get(data):
        async with semaphore:
            async with session.post(url, json=data, ssl=False) as response:
                obj = json.loads(await response.read())
                results.append(obj)
    await asyncio.gather(*(get(data) for data in pl))
    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(gather_with_concurrency(PARALLEL_REQUESTS))
conn.close()

print(f"Completed {len(pl)} requests with {len(results)} results")
