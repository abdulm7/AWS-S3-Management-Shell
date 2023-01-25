#!/usr/bin/env python3

#
#  Libraries and Modules
#
import boto3

#
#  List buckets
#

def list_buckets ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])

    for bucket in buckets:
        print ( bucket )
    ret = 0

    return ret

def bucket_list ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])
    return buckets

def upload_file ( s3, localPath, bucket, obj):
    try:
        s3.upload_file(localPath, bucket, obj)
        return True
    except:
        return False


def download_file( s3, localPath, bucket, obj):
    try:
        s3.download_file(bucket, obj, localPath)
        return True
    except:
        return False

    
# REFERENCE: Dr. Deb Stacey 'createBucket.py'
def create_bucket(s3, name):
    try:
        s3.create_bucket(Bucket=name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
        return True
    except :
        return False


def create_folder(s3, bucket, folder):
    try:
        s3.put_object(Bucket=bucket, Key=(folder+'/'))
        return True
    except:
        return False
