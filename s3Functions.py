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
import boto3

# Reference:
# Dr. Deb Stacey's Function
def list_buckets ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])

    for bucket in buckets:
        print ( bucket )
    ret = 0

    return ret

# Reference:
# Dr. Deb Stacey's Function
def bucket_list ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])
    return buckets

# 
def upload_file (s3, cmd, curDir):
    # error check appropriate parameter length
    if(len(cmd) != 3):
        return "(Usage) locs3cp <full or relative pathname of local file> /<bucket name>/<full pathname of S3 object>"
    else:
        # check relative or absolute path
        if (cmd[2][0] == '/'):
            bucketName = cmd[2].split("/")[1]
            objName = cmd[2][len(bucketName)+1:]
            objName = objName[1:]
        else:
            bucketName = curDir.split("/")[1]
            objName = curDir[len(bucketName)+1:] + cmd[2]
            objName = objName[1:]
        # storing local path
        localPath = cmd[1]

        # exception handling with boto3 api call
        try:
            s3.upload_file(localPath, bucketName, objName)
            return True
        except Exception as e:
            return e


def download_file( s3, cmd, curDir):
    # error check appropriate parameter length
    if(len(cmd) != 3):
        return "(Usage) s3loccp /<bucket name>/<full pathname of S3 file> <full/relative pathname of the local file>"
    else:
        # check relative or absolute path
        if (cmd[1][0] == '/'):
            bucketName = cmd[1].split("/")[1]
            objName = cmd[1][len(bucketName)+1:]
            objName = objName[1:]
        else:
            bucketName = curDir.split("/")[1]
            objName = curDir[len(bucketName)+1:] + cmd[1]
            objName = objName[1:]
        # storing local path
        localPath = cmd[2]

        # exception handling with boto3 api call
        try:
            s3.download_file(bucketName, objName, localPath)
            return True
        except Exception as e:
            return e


def create_bucket(s3, cmd):
    # error check appropriate parameter length
    if (len(cmd) != 2):
        return "(Usage) create_bucket /<bucket name>"
    else:
        # storing new bucket name
        name = cmd[1]
        # exception handling with boto3 api call
        try:
            s3.create_bucket(Bucket=name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
            return True
        except Exception as e:
            return e

def create_folder(s3, cmd, curDir):
    # error check appropriate parameter length
    if (len(cmd) != 2):
        return "(Usage #1) create_folder /<bucket name>/<full pathname for the folder>\n(Usage #2) create_folder <full or relative pathname for the folder>"
    else:
        # check relative or absolute path
        if (cmd[1][0] == '/'):
            bucketName = cmd[1].split("/")[1]
            objName = cmd[1][len(bucketName)+1:]
            objName = objName[1:]
        else:
            bucketName = curDir.split("/")[1]
            objName = curDir[len(bucketName)+1:] + cmd[1]
            objName = objName[1:]

        # exception handling with boto3 api call
        try:
            s3.put_object(Bucket=bucketName, Key=(objName+'/'))
            return True
        except Exception as e:
            return e


def delete_obj(s3, s3_res, cmd, curDir):
    # error check appropriate parameter length
    if (len(cmd) != 2):
        return ("s3delete <full or indirect pathname of object>")
    else:
        # check relative or absolute path
        if (cmd[1][0] == '/'):
            bucketName = cmd[1].split("/")[1]
            objName = cmd[1][len(bucketName)+1:]
            objName = objName[1:]
        else:
            bucketName = curDir.split("/")[1]
            objName = curDir[len(bucketName)+1:] + cmd[1]
            objName = objName[1:]


        bs = bucket_list(s3)

        # error check bucket name exists
        if bucketName not in bs:
            return "Invalid Bucket Name"

        # get bucket and objects in bucket
        bucket = s3_res.Bucket(bucketName)
        count = bucket.objects.filter(Prefix=objName)

        # ensure object exists
        if (len(list(count)) > 0 ):
            if (list(count)[0].key != objName):
                return objName + " not found"
        else:
            return objName + " not found"

        # ensure object exists, then ensure object is a folder
        if (objName[len(objName)-1] == '/'):
            # greater than 1 because folder itself counts as 1
            if len(list(count)) > 1:
                return "Folder is not empty"
    
        # exception handling with boto3 api call
        try:
            s3.delete_object(Bucket=bucketName, Key=objName)
            return True
        except Exception as e:
            return e


def delete_bucket(s3, cmd, curDir):
    # error check appropriate parameter length
    if (len(cmd) != 2):
        return "(Usage) delete_bucket <bucket name>"
    else:

        bucketName = cmd[1]

        # error check user is not trying to delete a bucket their are currently in
        if curDir != '/':
            curBucket = curDir.split("/")[1]
            if curBucket == bucketName:
                return "You are currently in the bucket you're attempting to delete"
        # exception handling with boto3 api call
        try:
            s3.delete_bucket(Bucket= bucketName)
            return True
        except Exception as e:
            return e

def change_location(s3, cmd, curDir):
    # error check appropriate parameter length
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

        # check for backwards traverse
        if ((len(cmd[1]) > 1) and (".." in cmd[1])):
            dests = cmd[1].split('/')
            cmd[1] = ""
            numBack = 0
            bucks = bucket_list(s3)
            for d in dests:
                if d == "..":
                    numBack +=1
                else:
                    if d in bucks:
                        cmd[1] = '/' + cmd[1] + d + '/'
                    else:
                        cmd[1] = cmd[1] + d + '/'
            
            if (numBack > len(curDir.split('/'))):
                curDir = '/'

            if (curDir != '/'):
                newCurDir = curDir.split('/')
                curDir = ""
                for i in range(len(newCurDir)-numBack-1):
                    curDir = curDir + newCurDir[i] + '/'

            if(curDir == ""):
                curDir = '/'

            if (cmd[1] == ""):
                return {'ret': True, 'curDir': curDir}


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


def copy_objects(s3, s3_res, cmd, curDir):
    # error check appropriate parameter length
    if (len(cmd) != 3):
        return ("s3copy <from S3 location of object> <to S3 location>")
    else:
        # parse bucket name and object path #1 (relative or absolute)
        if (cmd[1][0] == '/'):
            bname1 = cmd[1].split("/")[1]
            obj1 = cmd[1][len(bname1)+1:]
            obj1 = obj1[1:]
        else:
            bname1 = curDir.split("/")[1]
            obj1 = curDir[len(bname1)+1:] + cmd[1]
            obj1 = obj1[1:]

        # parse bucket name and object path #2 (relative or absolute)
        if (cmd[2][0] == '/'):
            bname2 = cmd[2].split("/")[1]
            obj2 = cmd[2][len(bname2)+1:]
            obj2 = obj2[1:]
        else:
            bname2 = curDir.split("/")[1]
            obj2 = curDir[len(bname2)+1:] + cmd[2]
            obj2 = obj2[1:]

        copySrc = {
            'Bucket': bname1,
            'Key': obj1
        }

        try:
            bucket = s3_res.Bucket(bname2)
            bucket.copy(copySrc, obj2)
            return True
        except Exception as e:
            return e


def list_all(s3, s3_res, cmd, curDir):
    # error check appropriate parameter length
    if (len(cmd) != 2 and len(cmd) != 1 and len(cmd) != 3):
        return ("""(Usage #1) list -l
        (Usage #2) list /<bucket name>
        (Usage #3) list /<bucket name>/<full pathname for directory or file>""")
    else:
        # checking all cases as well as exception handling all cases
        try:
            if(len(cmd) == 1):
                
                if(curDir == '/'):
                    list_buckets(s3)
                else:
                    bucketName = curDir.split("/")[1]
                    objName = curDir[len(bucketName)+1:]
                    objName = objName[1:]

                    bucket = s3_res.Bucket(bucketName)

                    if(objName == ""):
                        for b in bucket.objects.all():
                            print(b.key)
                    else:
                        for b in bucket.objects.filter(Prefix=objName):
                            print(b.key)

            elif (len(cmd) == 2 and cmd[1] != '-l'):

                if (curDir == '/' and cmd[1][0] != '/'):
                    cmd[1] = '/' + cmd[1]

                if (cmd[1][0] == '/'):
                    bucketName = cmd[1].split("/")[1]
                    objName = cmd[1][len(bucketName)+1:]
                    objName = objName[1:]

                else:
                    bucketName = curDir.split("/")[1]
                    objName = curDir[len(bucketName)+1:] + cmd[1]
                    objName = objName[1:]

                bucket = s3_res.Bucket(bucketName)

                if (objName == ""):
                    for b in bucket.objects.all():
                            print(b.key)
                else:
                    for b in bucket.objects.filter(Prefix=objName):
                            print(b.key)

            elif (len(cmd) == 2 and cmd[1] == '-l'):
                
                if(curDir == '/'):
                    response = s3.list_buckets()
                    for b in response['Buckets']:
                        print(f"\t{str(b['Name']):25s} Date Created: {str(b['CreationDate'])}")
                else:
                    bucketName = curDir.split("/")[1]
                    objName = curDir[len(bucketName)+1:]
                    objName = objName[1:]

                    bucket = s3_res.Bucket(bucketName)

                    if(objName == ""):
                        for b in bucket.objects.all():
                            print(f"{str(b.key):50s} \tLast Modified:  {str(b.last_modified):30s} \tSize: {str(b.size):20s}  \tOwner:  {str(b.owner):10s}")
                    else:
                        for b in bucket.objects.filter(Prefix=objName):
                            print(f"{str(b.key):50s} \tLast Modified:  {str(b.last_modified):30s} \tSize: {str(b.size):20s}:  \tOwner:  {str(b.owner):10s}")
            
            elif (len(cmd) == 3 and cmd[1] == '-l'):

                # parse bucket name and object path #1 (relative or absolute)
                if (cmd[2][0] == '/'):
                    bucketName = cmd[2].split("/")[1]
                    objName = cmd[2][len(bucketName)+1:]
                    objName = objName[1:]
                else:
                    bucketName = curDir.split("/")[1]
                    objName = curDir[len(bucketName)+1:] + cmd[2]
                    objName = objName[1:]

                bucket = s3_res.Bucket(bucketName)
                # formated print statements of information
                if(objName == ""):
                    for b in bucket.objects.all():
                        print(f"{str(b.key):50s} \tLast Modified:  {str(b.last_modified):30s} \tSize: {str(b.size):20s}  \tOwner:  {str(b.owner):10s}")
                else:
                    for b in bucket.objects.filter(Prefix=objName):
                        print(f"{str(b.key):50s} \tLast Modified:  {str(b.last_modified):30s} \tSize: {str(b.size):20s}:  \tOwner:  {str(b.owner):10s}")
        except Exception as e:
            return e



