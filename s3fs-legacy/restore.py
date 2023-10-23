import gzip
import sys
import os.path
import time

"""
lv: the target mapped lv block device to restore to. usually /dev/<vgname>/<lvname>
targetdir: the directory where the snapshot files are found
snapshot: name of the snapshot: usually <YYYYMMDD-snapshot>
"""

blocksize = 3221225472

def unread_and_spit(lv: str, targetdir: str, snapshot: str):
    partsfname = os.path.join(targetdir, f"{snapshot}.parts")
    with open(partsfname) as fp:
        parts = int(fp.read())

    with open(lv, "wb") as lvfp:
        for currpart in range(1,parts+1):
            targetfname = os.path.join(targetdir, f"{snapshot}.{currpart}")
            t1 = time.time()
            with open(targetfname, "rb") as target:
                b = target.read()
            t2 = time.time()
            readsize = len(b)
            print(f"read {readsize} from {targetfname} in {t2-t1}s")
            b = gzip.decompress(b)
            t1 = time.time()
            decompsize = len(b)
            print(f"decompressed {targetfname} from {readsize} to {decompsize} in {t1-t2}s")
            writesize = lvfp.write(b)
            t2 = time.time()
            print(f"wrote {writesize} to {lv} in {t2-t1}s")
            if writesize!=decompsize:
                print(f"data size was {decompsize} but wrote {writesize}!")
                sys.exit(1)


if __name__ == "__main__":
    lv = sys.argv[1]
    targetdir = sys.argv[2]
    snapshot = sys.argv[3]
    print(f"lv: {lv}, targetdir {targetdir}, snapshot: {snapshot}")
    start = time.time()
    unread_and_spit(lv, targetdir, snapshot)
    end = time.time()
    print(f"total time is {end-start}s")
