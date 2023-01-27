#!/usr/bin/env python3

#
#  Libraries and Modules
#
import boto3

#
#  List buckets
#

# # global variable to track users PWD
# curDir = ""

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

def upload_file (s3, cmd):

    if(len(cmd) != 3):
        return "(Usage) locs3cp <full or relative pathname of local file> /<bucket name>/<full pathname of S3 object>"
    else:
        # call local to s3 copy
        bucketName = cmd[2].split("/")[0]
        localPath = cmd[1]
        objName = cmd[2][len(bucketName)+1:]

        try:
            s3.upload_file(localPath, bucketName, objName)
            return True
        except Exception as e:
            return e


def download_file( s3, cmd):

    if(len(cmd) != 3):
        return "(Usage) s3loccp /<bucket name>/<full pathname of S3 file> <full/relative pathname of the local file>"
    else:
        # call local to s3 copy
        bucketName = cmd[1].split("/")[0]
        localPath = cmd[2]
        obj = cmd[1][len(bucketName)+1:]

        try:
            s3.download_file(bucketName, obj, localPath)
            return True
        except Exception as e:
            return e


    
# REFERENCE: Dr. Deb Stacey 'createBucket.py'
def create_bucket(s3, cmd):
    if (len(cmd) != 2):
        return "(Usage) create_bucket /<bucket name>"
    else:
        name = cmd[1]
        try:
            s3.create_bucket(Bucket=name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
            return True
        except Exception as e:
            return e

def create_folder(s3, cmd):
    if (len(cmd) != 2):
        return "(Usage #1) create_folder /<bucket name>/<full pathname for the folder>\n(Usage #2) create_folder <full or relative pathname for the folder>"
    else:
        # *** CHECK FIRST NAME IS BUCKET, IF NOT CHECK IF FOLDER NAME (RELATIVE) *** #
        # THIS IS TEMP, WILL NEED TO KEEP TRACK OF WHAT BUCKET I'M IN SOME HOW
        # TRACK THROUGHOUT CHANGE LOCATION/CHANGE DIRECTORY
        bucketName = cmd[1].split("/")[0]
        path = cmd[1][len(bucketName)+1:]

        try:
            s3.put_object(Bucket=bucketName, Key=(path+'/'))
            return True
        except Exception as e:
            return e


def delete_obj(s3, bucket, obj):
    try:
        s3.Object(bucket, obj).delete()
        return True
    except Exception as e:
        return e


def delete_bucket(s3, cmd, curDir):
    if (len(cmd) != 2):
        return "(Usage) delete_bucket <bucket name>"
    else:
        bucketName = cmd[1]
        try:
            s3.delete_bucket(Bucket= bucketName)
            return True
        except Exception as e:
            return e

def change_location(s3, cmd, curDir):
    if (len(cmd) != 2):
        return {
            'ret':"""(Usage #1) chlocn /<bucket name>
               (Usage #2) chlocn /<bucket name>/<full pathname of directory>
               (Usage #3) chlocn <full or relative pathname of directory>""",
            'curDir': curDir
        }

    else:
        # add '/' so buckets can be refered to relatively
        if (curDir == '/' and cmd[1][0] != '/'):
            cmd[1] = '/' + cmd[1]

        if ((len(cmd[1]) > 1) and (".." in cmd[1])):
            dests = cmd[1].split('/')
            cmd[1] = ""
            numBack = 0
            for d in dests:
                if d == "..":
                    numBack +=1
                else:
                    cmd[1] = cmd[1] + d + '/'
            
            if (curDir != '/'):
                newCurDir = curDir.split('/')
                curDir = ""
                for i in range(len(newCurDir)-numBack-1):
                    curDir = curDir + newCurDir[i] + '/'

            if(curDir == ""):
                curDir = '/'

            if (cmd[1] == ""):
                return {'ret': True, 'curDir': curDir}

            print("THIS IS COMMAND: " + cmd[1])


        # check if bucket/full path
        if cmd[1][0] == '/' and len(cmd[1]) > 1:
            bucketName = cmd[1].split("/")[1]
            # skip 2 spaces to account for character at [0] and the '/'
            
            if (('/' + bucketName != cmd[1]) and ('/' + bucketName + '/') != cmd[1]):
                path = cmd[1][len(bucketName)+2:]
                if (path[len(path)-1] != '/'):
                    path = path + '/'
                    # Create a reusable Paginator
                try:
                    paginator = s3.get_paginator('list_objects')
                    # Create a PageIterator from the Paginator
                    page_iterator = paginator.paginate(Bucket=bucketName)
                except Exception as e:
                    return {'ret': e, 'curDir': curDir}

                for page in page_iterator:
                    for data in page['Contents']:
                        if (str(data['Key']) == str(path)):
                            curDir = '/' + bucketName + '/' + path
                            return {'ret': True, 'curDir': curDir}
            else:
                buckets = bucket_list(s3)
                
                for b in buckets:
                    if str(b) == bucketName:
                        curDir = '/' + bucketName + '/'
                        return {'ret': True, 'curDir': curDir}

        elif (cmd[1] == '~' or cmd[1] == "/"):
            return {'ret': True, 'curDir': '/'}
        else:
            # relative path
            bucketName = curDir.split("/")[1]
            path = curDir[len(bucketName)+2:] + cmd[1]
            if (path[len(path)-1] != '/'):
                path = path + '/'
            try:
                paginator = s3.get_paginator('list_objects')
                # Create a PageIterator from the Paginator
                page_iterator = paginator.paginate(Bucket=bucketName)
            except Exception as e:
                return {'ret': e, 'curDir': curDir}

            for page in page_iterator:
                for data in page['Contents']:
                    if (str(data['Key']) == str(path)):
                        curDir = '/' + bucketName + '/' + path
                        return {'ret': True, 'curDir': curDir}
        
        return {'ret': False, 'curDir': curDir}
