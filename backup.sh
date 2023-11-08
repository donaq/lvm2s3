#!/bin/bash
. config.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

SNAPSHOTNAME=`date +%Y%m%d`-snapshot

SNAPSHOTLV=$VGDEV/$SNAPSHOTNAME


# make lvm snapshot
echo "create snapshot with:"
echo "lvcreate -s -L $SNAPSHOTSIZE -n $SNAPSHOTNAME $LV"

# back up snapshot
echo "backup snapshot with:"
echo "python $SCRIPT_DIR/backup.py $SNAPSHOTLV $SNAPSHOTNAME"
