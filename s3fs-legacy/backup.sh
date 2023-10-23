#!/bin/bash
. config.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

HOSTNAME=$(cat /etc/hostname)

SNAPSHOTNAME=`date +%Y%m%d`-snapshot

SNAPSHOTLV=$VGDEV/$SNAPSHOTNAME

BACKUPDIR=$S3MOUNTDIR/$HOSTNAME-backups


# mount the s3 bucket
mkdir -p $S3MOUNTDIR
s3fs $S3BUCKET $S3MOUNTDIR -o passwd_file=$S3PW -o url=$S3URL -o use_path_request_style
mkdir -p $BACKUPDIR

# make lvm snapshot
echo "create snapshot with:"
echo "sudo lvcreate -s -L $SNAPSHOTSIZE -n $SNAPSHOTNAME $LV"
#sudo lvcreate -s -L $SNAPSHOTSIZE -n $SNAPSHOTNAME $LV

# back up snapshot
echo "backup snapshot with:"
echo "sudo python $SCRIPT_DIR/backup.py $SNAPSHOTLV $BACKUPDIR $SNAPSHOTNAME"
