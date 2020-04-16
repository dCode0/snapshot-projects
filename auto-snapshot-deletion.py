import boto3
import os

ec2 = boto3.client('ec2', 'us-east-2')
snapshots = ec2.describe_snapshots(OwnerIds=['self'])


num = int(os.environ["SNAPSHOT"])


def lambda_handler(event, context):

    images = [image.id for image in ec2.images.all()]
    dates = sorted([snapshot['StartTime'] for snapshot in snapshots['Images']])[-num:]
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        create_date = snapshot['StartTime']

        if create_date not in dates:
            print(f'deleting {snapshot_id}')
            ec2.delete_snapshot(SnapshotId=snapshot_id)
