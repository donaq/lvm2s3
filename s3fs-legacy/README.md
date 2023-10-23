## Configuration

sample `config.sh`

```bash
export S3PW=$HOME/.passwd-s3fs
export S3URL=https://s3.ap-northeast-2.wasabisys.com
export S3BUCKET=yourbucket
export S3MOUNTDIR=$HOME/wasabi-aqskstuff
export VG=homevg # name of volume group
export VGDEV=/dev/$VG # volume group device
export LV=$VGDEV/homelv # logical volume device path
export SNAPSHOTSIZE=100G # snapshot size
```

`S3PW` should point to a file containing your s3 access key id and access secret key, in that order, separated by a `:`

## Usage

./backup.sh
