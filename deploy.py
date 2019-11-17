#!/usr/bin/python3
'''
Author: Tom Stewart
Description:
    gets a list of all local files in project
    compares local md5 sum with s3 etag/md5sum
    upload new if md5's do not match
'''
import os
import hashlib
import boto3
import botocore


def _s3_md5sum(resource_name, bucket_name):
    '''get s3 md5sum'''
    try:
        md5sum = boto3.client('s3').head_object(
            Bucket=bucket_name,
            Key=resource_name
        )['ETag'][1:-1]
    except botocore.exceptions.ClientError:
        md5sum = None
    return md5sum

def _local_md5sum(resource_name):
    '''get local file md5sum'''
    md5 = hashlib.md5(open(resource_name, 'rb').read(1024 * 1024)).hexdigest()
    return md5

def _set_content_type(resource_name):
    '''upload changed file to s3'''
    if 'css' in resource_name:
        contenttype='text/css'
    elif 'html' in resource_name:
        contenttype='text/html'
    elif 'jpg' in resource_name:
        contenttype='image/jpg'
    elif 'png' in resource_name:
        contenttype='image/png'
    else:
        contenttype='text/html'
    print(contenttype)
    return contenttype

def _upload_file(resource_name, bucket_name):
    '''upload changed file to s3'''
    contenttype = _set_content_type(resource_name)
    body = open(resource_name, 'rb')
    s3_resource = boto3.resource('s3')
    # local file, bucket name, key name
    s3_resource.meta.client.put_object(
        Bucket=bucket_name,
        Key=resource_name,
        Body=body,
        ContentType=contenttype
    )

def main():
    '''find all files in project
       check if file md5 does not match s3
       if no match, upload new version
    '''
    bucketname = 'twstewart.me'
    directory = '.'
    exclude = ['.git', '.terraform', 'terraform.tfstate', 'terraform.tfstate.backup', '.vscode']
    for dirpath, dirnames, files in os.walk(directory):
        for dirn in list(dirnames):
            print(dirn)
            if dirn in exclude:
                dirnames.remove(dirn)
        for name in files:
            if name not in exclude:
                filename = os.path.join(dirpath, name)[2:]
                print(filename)
                s3_md5 = _s3_md5sum(filename, bucketname)
                lcl_md5 = _local_md5sum(filename)
                print(lcl_md5, s3_md5)
                if lcl_md5 != s3_md5:
                    print("upload new")
                    _upload_file(filename, bucketname)

if __name__ == "__main__":
    main()
