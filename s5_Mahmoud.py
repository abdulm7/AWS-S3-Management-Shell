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

def main():
    #
    #  Find AWS access key id and secret access key information
    #  from configuration file
    #
    config = configparser.ConfigParser()
    config.read("S5-S3.conf")
    aws_access_key_id = config["test-1"]["aws_access_key_id"]
    aws_secret_access_key = config["test-1"]["aws_secret_access_key"]

    curDir = "/"

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

        while raw_cmd.lower() != "quit" and raw_cmd.lower() != "exit":
            
            raw_cmd = input( "S5 > ")
            cmd = raw_cmd.split()

            if (len(cmd) == 0):
                cmd = "  "

            if (cmd[0] == "locs3cp"):

                ret = s3f.upload_file(s3, cmd)

                if (ret == True):
                    print("\tPASSED: Local to S3 copy was successful!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0] == "s3loccp"):

                ret = s3f.download_file( s3, cmd)

                if (ret == True):
                    print("\tPASSED: S3 to Local copy was successful!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0] == "create_bucket"):

                ret = s3f.create_bucket(s3, cmd)

                if (ret == True):
                    print("\tPASSED: Bucket was successfully created!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0] == "create_folder"):

                ret = s3f.create_folder(s3, cmd)

                if (ret == True):
                    print("\tPASSED: Folder was successfully created!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0] == "delete_bucket"):

                ret = s3f.delete_bucket(s3, cmd)

                if (ret == True):
                    print("\tPASSED: Bucket was successfully deleted!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0] == "chlocn"):
                
                print("Pre-change location: " + curDir)

                ret = s3f.change_location(s3, cmd, curDir)

                if (ret['ret'] == True):
                    print("\tPASSED: Successfully changed location!")
                elif(ret['ret'] == False):
                    print("\tERROR: failed to change location.")
                else:
                    print("\tERROR: " + ret['ret'])

                curDir = ret['curDir']
                print("Post-change location" + curDir)

            elif(cmd[0] == "cd"):
                try:
                    os.chdir(cmd[1])
                except Exception as e:
                    print("ERROR: Path doesn't exist or is not a directory.")
            else:
                os.system(raw_cmd)
    
    except Exception as e:
        print ( "cannot connect to s3: " + str(e))

main()

