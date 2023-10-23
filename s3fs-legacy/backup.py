import gzip
import sys
import os.path
import time

blocksize = 3221225472

def read_and_spit(lv: str, targetdir: str, snapshot: str):
    currpart = 1
    with open(lv, "rb") as src:
        totalread = 0

        # init current target file
        targetfname = os.path.join(targetdir, f"{snapshot}.{currpart}")
        print(f"writing {targetfname}")
        target = open(targetfname, "wb")

        while True:
            t1 = time.time()
            b = src.read(blocksize)
            t2 = time.time()
            readsize = len(b)
            print(f"read {readsize} from {lv} in {t2-t1}s")
            totalread += readsize

            b = gzip.compress(b)
            t1 = time.time()
            compsize = len(b)
            print(f"compressed {readsize} to {compsize} in {t1-t2}s")

            writesize = target.write(b)
            # unable to write full block to file
            if writesize!=compsize:
                print(f"compressed size = {compsize} but writesize = {writesize} for {targetfname}!")
                target.close()
                break

            # reach end of lv
            if readsize<blocksize:
                print(f"finished reading {totalread} bytes from {lv}")
                target.close()
                break

            target.close()
            t2 = time.time()
            print(f"wrote {compsize} to {targetfname} in {t2-t1}s")
            currpart += 1
            targetfname = os.path.join(targetdir, f"{snapshot}.{currpart}")
            print(f"writing {targetfname}")
            target = open(targetfname, "wb")


    with open(os.path.join(targetdir, f"{snapshot}.parts"), "w") as fp:
        fp.write(f"{currpart}")


if __name__ == "__main__":
    lv = sys.argv[1]
    targetdir = sys.argv[2]
    snapshot = sys.argv[3]
    print(f"lv: {lv}, targetdir {targetdir}, snapshot: {snapshot}")
    start = time.time()
    read_and_spit(lv, targetdir, snapshot)
    end = time.time()
    print(f"total time is {end-start}s")
