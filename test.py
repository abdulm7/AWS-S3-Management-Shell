#!/usr/bin/env python3

#
#  Libraries and Modules
#
import configparser
import os 
import sys 
import pathlib
import boto3

#
#  Find AWS access key id and secret access key information
#  from configuration file
#

try:
#
#  Establish an AWS session
#
    session = boto3.Session(
        aws_access_key_id="YOUR_ACCESS_KEY",
        aws_secret_access_key="YOUR_SECRET_ACCESS_KEY"
    )
#
#  Set up client and resources
#
    s3 = session.client('s3')
    s3_res = session.resource('s3')

    print ( "Welcome to the S3 Storage Demo - List Buckets" )

#
#  List buckets
#
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])

    for bucket in buckets:
        print ( bucket )

except:
    print ( "cannot connect to s3" )
