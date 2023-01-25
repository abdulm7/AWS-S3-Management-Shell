# Abdul Mahmoud
# 1093276
# Jan 21, 2023
# CIS*4010
# Assignment #1
# AWS Shell

#!/usr/bin/env python3
#
#  Libraries and Modules
#
import configparser
import os 
import sys 
import pathlib
import boto3
import s3Functions as s3f
#

def main():
    #
    #  Find AWS access key id and secret access key information
    #  from configuration file
    #
    config = configparser.ConfigParser()
    config.read("S5-S3.conf")
    aws_access_key_id = config["test-1"]["aws_access_key_id"]
    aws_secret_access_key = config["test-1"]["aws_secret_access_key"]

    try:
    #
    #  Establish an AWS session
    #
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    #
    #  Set up client and resources
    #
        s3 = session.client("s3")
        s3_res = session.resource("s3")

        print ( "Welcome to S5 Shell" )

        # initialize 
        raw_cmd = ""
        curDir = "/"

        while raw_cmd.lower() != "quit" and raw_cmd.lower() != "exit":
            
            raw_cmd = input(curDir + " > ")
            cmd = raw_cmd.split()

            if (len(cmd) == 0):
                cmd = "  "

            if (cmd[0] == "locs3cp"):
                if(len(cmd) != 3):
                    print("Usage: locs3cp <full or relative pathname of local file> /<bucket name>/<full pathname of S3 object>")
                else:
                    # call local to s3 copy
                    bucketName = cmd[2].split("/")[0]
                    localPath = cmd[1]
                    objName = cmd[2][len(bucketName)+1:]

                    ret = s3f.upload_file(s3, localPath, bucketName, objName)

                    if (ret == True):
                        print("\tPASSED: Local to S3 copy was successful!")
                    else:
                        print("\tERROR: Local to S3 copy was unsuccessful.")

            elif (cmd[0] == "s3loccp"):
                if(len(cmd) != 3):
                    print("Usage: s3loccp /<bucket name>/<full pathname of S3 file> <full/relative pathname of the local file>")
                else:
                    # call local to s3 copy
                    bucketName = cmd[1].split("/")[0]
                    localPath = cmd[2]
                    obj = cmd[1][len(bucketName)+1:]

                    ret = s3f.download_file( s3, localPath, bucketName, obj)

                    if (ret == True):
                        print("\tPASSED: S3 to Local copy was successful!")
                    else:
                        print("\tERROR: S3 to Local copy was unsuccessful.")

            elif (cmd[0] == "create_bucket"):
                if (len(cmd) != 2):
                    print("Usage: create_bucket /<bucket name>")
                else:
                    name = cmd[1]
                    ret = s3f.create_bucket(s3, name)

                    if (ret == True):
                        print("\tPASSED: Bucket was successfully created!")
                    else:
                        print("\tERROR: Failed to create bucket.")

            elif (cmd[0] == "create_folder"):
                if (len(cmd) != 2):
                    print("Usage #1: create_folder /<bucket name>/<full pathname for the folder>\nUsage #2: create_folder <full or relative pathname for the folder>")
                else:
                    # *** CHECK FIRST NAME IS BUCKET, IF NOT CHECK IF FOLDER NAME (RELATIVE) *** #
                    # THIS IS TEMP, WILL NEED TO KEEP TRACK OF WHAT BUCKET I'M IN SOME HOW
                    # TRACK THROUGHOUT CHANGE LOCATION/CHANGE DIRECTORY
                    bucketName = cmd[1].split("/")[0]
                    path = obj = cmd[1][len(bucketName)+1:]

                    ret = s3f.create_folder(s3, bucketName, path)

                    if (ret == True):
                        print("\tPASSED: Folder was successfully created!")
                    else:
                        print("\tERROR: Failed to create folder.")

            elif (cmd[0] == "delete_bucket"):
                if (len(cmd) != 2):
                    print("Usage: delete_bucket <bucket name>")
                else:
                    bucketName = cmd[1]
                    print(bucketName)
                    ret = s3f.delete_bucket(s3, bucketName)

                    if (ret == True):
                        print("\tPASSED: Bucket was successfully deleted!")
                    else:
                        print("\tERROR: Failed to delete bucket (Ensure bucket is Empty).")

            
            elif(cmd[0] == "cd"):
                try:
                    os.chdir(cmd[1])
                except Exception as e:
                    print("ERROR: Path doesn't exist or is not a directory.")
            else:
                os.system(raw_cmd)
    
    except Exception as e:
        print ( "cannot connect to s3: " + e)

main()

