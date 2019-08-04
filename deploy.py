#!/usr/bin/python3
import boto3
import botocore
import hashlib
import os

def _s3_md5sum(resource_name):
    try:
        md5sum = boto3.client('s3').head_object(
            Bucket='twstewart.me',
            Key=resource_name
        )['ETag'][1:-1]
    except botocore.exceptions.ClientError:
        md5sum = None
        pass
    return md5sum

def _local_md5sum(resource_name):
    md5 = hashlib.md5(open(resource_name,'rb').read(1024 * 1024)).hexdigest()
    return md5

def _upload_file(resource_name):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(resource_name, 'twstewart.me', resource_name)

def main():
    #filename = 'index.html'
    directory = '.'
    exclude = ['.git', '.terraform']
    for dirpath, dirnames, files in os.walk(directory):
        [dirnames.remove(d) for d in list(dirnames) if d in exclude]
        for name in files:
            #print(os.path.join(dirpath,name))
            filename = os.path.join(dirpath,name)[2:]
            print (filename)
            s3_md5 = _s3_md5sum(filename)
            lcl_md5 = _local_md5sum(filename)
            print (lcl_md5, s3_md5)
            if lcl_md5 != s3_md5:
                print("upload new")
                _upload_file(filename)

if __name__ == "__main__":
    main()
