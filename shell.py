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
    aws_access_key_id = config["default"]["aws_access_key_id"]
    aws_secret_access_key = config["default"]["aws_secret_access_key"]

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

        # will throw exception if connection is not real
        s3f.bucket_list(s3)

        print ( "Welcome to S5 Shell" )

        # initialize 
        raw_cmd = ""

        # menu / command options
        while raw_cmd.lower() != "quit" and raw_cmd.lower() != "exit":
            
            # unparsed command
            raw_cmd = input( "S5 > ")
            # split command (no white space)
            cmd = raw_cmd.split()

            # avoid any empty string error
            if (len(cmd) == 0):
                cmd = "  "

            # cmd[0] is command anything after will be parameter
            if (cmd[0].lower() == "locs3cp"):

                ret = s3f.upload_file(s3, cmd, curDir)

                if (ret == True):
                    print("\tPASSED: Local to S3 copy was successful!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0].lower() == "s3loccp"):

                ret = s3f.download_file( s3, cmd, curDir)

                if (ret == True):
                    print("\tPASSED: S3 to Local copy was successful!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0].lower() == "create_bucket"):

                ret = s3f.create_bucket(s3, cmd)

                if (ret == True):
                    print("\tPASSED: Bucket was successfully created!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0].lower() == "create_folder"):

                ret = s3f.create_folder(s3, cmd, curDir)

                if (ret == True):
                    print("\tPASSED: Folder was successfully created!")
                else:
                    print("\tERROR: " + str(ret) + ".")

            elif (cmd[0].lower() == "delete_bucket"):

                ret = s3f.delete_bucket(s3, cmd, curDir)

                if (ret == True):
                    print("\tPASSED: Bucket was successfully deleted!")
                else:
                    print("\tERROR: " + str(ret) + ".")
                
            elif (cmd[0].lower() == 's3delete'):

                ret = s3f.delete_obj(s3, s3_res, cmd, curDir)

                if (ret == True):
                    print("\tPASSED: Object was successfully deleted!")
                else:
                    print("\tERROR: " + str(ret) + ".")


            elif (cmd[0].lower() == 'cwlocn'):
                
                if(len(cmd) > 1):
                    print("\tERROR: (Usage) cwlocn")
                else:
                    print("\t" + curDir)

            
            elif (cmd[0].lower() == 's3copy'):

                ret = s3f.copy_objects(s3, s3_res, cmd, curDir)

                if (ret == True):
                    print("\tPASSED: Object was successfully copied!")
                else:
                    print("\tERROR: " + str(ret) + ".")
                

            elif (cmd[0].lower() == "chlocn"):

                ret = s3f.change_location(s3, cmd, curDir)
                curDir = ret['curDir']

                if (ret['ret'] == True):
                    print("\tPASSED: Successful! Current Working Directory: " + curDir)
                elif(ret['ret'] == False):
                    print("\tYou have not changed directories.")
                else:
                    print("\tERROR: " + str(ret['ret']))

            elif (cmd[0].lower() == "list"):

                ret = s3f.list_all(s3, s3_res, cmd, curDir)

            elif(cmd[0].lower() == "cd"):
                try:
                    os.chdir(cmd[1])
                except Exception as e:
                    print("ERROR: Path doesn't exist or is not a directory.")
            else:
                os.system(raw_cmd)
    
    except Exception as e:
        print ( "cannot connect to s3: " + str(e))

main()

