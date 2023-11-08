# LVM To S3

A set of scripts for backing up a LVM volume to s3-compatible storage (tested only on Wasabi). I wrote this to scratch my own itch and it is usable as such. If you find this useful, great! Just please don't ask for new features. Feel free to fork.

## Dependencies

`pip install -r requirements.txt`

## Back up

### Preparation

Create a `config.sh` file like so:

```bash
export AWS_ACCESS_KEY_ID=<your key id>
export AWS_SECRET_ACCESS_KEY=<your access key>
export AWS_ENDPOINT=<the endpoint given by your s3 provider>
export BUCKET=<your bucket>
export VG=<volume group name>
export VGDEV=/dev/$VG
export LV=$VGDEV/<logical volume name>
export SNAPSHOTSIZE=200G # for example
```

### Usage

Run `./backup.sh` as root and follow the instructions.

## Restore

I decided that writing this README was better than writing another bash script to output instructions.

As root:

```bash
export AWS_ACCESS_KEY_ID=<your key id>
export AWS_SECRET_ACCESS_KEY=<your access key>
export AWS_ENDPOINT=<the endpoint given by your s3 provider>
export BUCKET=<your bucket>
export VGNAME=<volume group name>
export LVNAME=<logical volume name>
export VGDEV=/dev/$VG
export LV=$VGDEV/$LVNAME
export LVSIZE=2T # f'rinstance

# prepare lv

# note that I have two PVs, so I stripe my LV. if you are using only one PV, omit the -i

lvcreate -i 2 -L $LVSIZE -n $LVNAME $VGNAME

# get available snapshots

aws --endpoint $AWS_ENDPOINT s3 ls s3://$BUCKET/

python restore.py $LV 20231105-snapshot
```

## Reminder to self on how to extend LUKS on LVM

After copying snapshot to lv:

1. comment out mountpoint from `/etc/fstab` and mapping from `/etc/crypttab`
2. reboot and login as root
3. `lvextend -L 3T /dev/<vg name>/<lv name>`
4. `crypsetup open /dev/<vg name>/<lv name> <cryptvolname>`
5. `e2fsck -f /dev/mapper/<cryptvolname>`
6. `resize2fs /dev/mapper/<cryptvolname>`
7. mount the resulting volume and check if everything's fine
8. restore `/etc/fstab` and `/etc/crypttab`
9. reboot
