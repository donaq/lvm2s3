import gzip
import sys
import os.path

maxfilesize = 3221225472
blocksize = 3145728

def read_and_spit(lv: str, targetdir: str, snapshot: str):
    with open(lv, "rb") as src:
        totalread = 0

        # init current target file
        currpart = 1
        currsize = 0
        targetfname = os.path.join([targetdir, f"{snapshot}.{currpart}.gz"])
        print(f"writing {targetfname}")
        target = open(targetfname, "wb")

        while True:
            b = src.read(blocksize)
            readsize = len(b)
            totalread += readsize

            writesize = target.write(b)
            currsize += writesize

            # unable to write full block to file
            if writesize!=readsize:
                print(f"readsize = {readsize} but writesize = {writesize}!")
                target.close()
                break

            # reach end of lv
            if readsize<blocksize:
                print(f"finished reading {totalread} bytes from {lv}")
                target.close()
                break

            if currsize >= maxfilesize:
                print(f"wrote {currsize} to {targetfname} which is >= {maxfilesize}")
                target.close()
                currpart += 1
                currsize = 0
                targetfname = os.path.join([targetdir, f"{snapshot}.{currpart}.gz"])
                print(f"writing {targetfname}")
                target = open(targetfname, "wb")



if __name__ == "__main__":
    lv = sys.argv[1]
    targetdir = sys.argv[2]
    snapshot = sys.argv[3]
    print(f"lv: {lv}, targetdir {targetdir}, snapshot: {snapshot}")
