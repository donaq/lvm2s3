import boto3
import os
import sys
import gzip
import time
from hashlib import md5

bucket = os.environ["BUCKET"]
endpoint = os.environ["AWS_ENDPOINT"]
blocksize = 3221225472

def read_and_spit(lv: str, snapshot: str):
    cli = boto3.client(service_name="s3",endpoint_url=endpoint)
    with open(lv, "rb") as src:
        currpart = 1
        totalread = 0

        # init current target file
        targetfname = f"{snapshot}/{currpart}"
        hashname = f"{targetfname}.md5"
        print(f"writing {targetfname}")

        while True:
            t1 = time.time()
            b = src.read(blocksize)
            t2 = time.time()
            readsize = len(b)
            print(f"read {readsize} from {lv} in {t2-t1}s")
            totalread += readsize

            # I used to gzip but that just wastes time and space after I decided to encrypt the volume
            # feel free to re-enable it if you feel up to it
            """
            b = gzip.compress(b)
            t1 = time.time()
            compsize = len(b)
            print(f"compressed {readsize} to {compsize} in {t1-t2}s")
            """

            _ = cli.put_object(Body=b, Bucket=bucket, Key=targetfname)
            t1 = time.time()
            print(f"wrote {readsize} to {targetfname} in {t1-t2}s")

            # write the hash
            hb = md5(b).digest()
            t2 = time.time()
            print(f"generated hash {hashname} in {t2-t1}s")
            _ = cli.put_object(Body=hb, Bucket=bucket, Key=hashname)
            t1 = time.time()
            print(f"wrote {hashname} in {t1-t2}s")

            # reach end of lv
            if readsize<blocksize:
                print(f"finished reading {totalread} bytes from {lv}")
                break

            currpart += 1
            targetfname = f"{snapshot}/{currpart}"
            hashname = f"{targetfname}.md5"
            print(f"writing {targetfname}")

        b = bytes(f"{currpart}", "utf-8")
        rsp = cli.put_object(Body=b, Bucket=bucket, Key=f"{snapshot}/parts")


if __name__ == "__main__":
    lv = sys.argv[1]
    snapshot = sys.argv[2]
    print(f"lv: {lv}, snapshot: {snapshot}")
    start = time.time()
    read_and_spit(lv, snapshot)
    end = time.time()
    print(f"total time is {end-start}s")
