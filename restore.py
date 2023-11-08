import gzip
import boto3
import sys
import os
import os.path
import time
from hashlib import md5

"""
lv: the target mapped lv block device to restore to. usually /dev/<vgname>/<lvname>
snapshot: name of the snapshot: usually <YYYYMMDD-snapshot>
"""

bucket = os.environ["BUCKET"]
endpoint = os.environ["AWS_ENDPOINT"]
blocksize = 3221225472

def unread_and_spit(lv: str, snapshot: str):
    cli = boto3.client(service_name="s3",endpoint_url=endpoint)

    def obj_bytes(key: str):
        rsp = cli.get_object(Bucket=bucket, Key=key)
        return rsp['Body'].read()

    # get parts
    partsfname = f"{snapshot}/parts"
    parts = obj_bytes(partsfname).decode("utf-8")
    parts = int(parts)
    print(f"{snapshot} has {parts} parts")

    with open(lv, "wb") as lvfp:
        for currpart in range(1,parts+1):
            targetfname = f"{snapshot}/{currpart}"
            hashname = f"{targetfname}.md5"
            t1 = time.time()
            b = obj_bytes(targetfname)
            t2 = time.time()
            readsize = len(b)
            print(f"read {readsize} from {targetfname} in {t2-t1}s")

            hb = obj_bytes(hashname)
            t1 = time.time()
            hbloc = md5(b).digest()
            t2 = time.time()
            print(f"hashed {targetfname} content in {t2-t1}s")

            if hb!=hbloc:
                print(f"hash of downloaded {targetfname} does not match {hashname}. you should use another snapshot")
                sys.exit(1)

            writesize = lvfp.write(b)
            t1 = time.time()
            print(f"wrote {writesize} to {lv} in {t1-t2}s")
            if writesize!=readsize:
                print(f"data size was {decompsize} but wrote {writesize}!")
                sys.exit(1)


if __name__ == "__main__":
    lv = sys.argv[1]
    snapshot = sys.argv[2]
    print(f"lv: {lv}, snapshot: {snapshot}")
    start = time.time()
    unread_and_spit(lv, snapshot)
    end = time.time()
    print(f"total time is {end-start}s")
