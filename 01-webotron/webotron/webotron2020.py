#!/usr/bin/python         //tells user how to run Code
#-*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS"""  #-denote docstrings with 3x quotes

#---import modules---#
from pathlib import Path
import boto3
from botocore.exceptions import ClientError   #-group similar libraries together
import click
import mimetypes
from botocore.exceptions import ClientError

#---Establish Session---#
session = boto3.Session(profile_name ='pythonAutomation')
s3 = session.resource('s3')

#---CLICK commands---#
@click.group()             #-creates a menu of available commands-#
def cli():                 #-group name = cli-#
    """Webotron deploys websites to AWS"""
    pass                   #-do nothing-#

#---cli group option 1---#
@cli.command('list-buckets')         #-DECORATOR wraps a function-#
def list_buckets():                  #-DOCSTRING-#
    """Description: List all s3 buckets."""
    for bucket in s3.buckets.all():
        print(bucket)

#---cli group option 2---#
@cli.command('list-bucket-objects')
@click.argument('bucket')            #-user input via argument click feature-#
def list_bucket_objects(bucket):
    """List more crap"""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

#---cli group option 3---#
@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure new S3 bucket"""

    #---get region_name---#
    session.region_name

    #---Create new s3 bucket with LocationConstraint---#
    s3_bucket =s3.create_bucket(Bucket=bucket, CreateBucketConfiguration ={'LocationConstraint':session.region_name})

    #---Replace bucket with placeholder %s---#
    policy = """
        {
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::%s/*"]
                }
                ]
        }
        """ % s3_bucket.name
    #---Fix the JSON error to remove whitespace chars from string---#
    policy = policy.strip()

    #---Create bucket policy---#
    pol = s3_bucket.Policy()

    #---Apply policy to objects---#
    pol.put(Policy=policy)

    #---Setup website Configuration---#
    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
            'ErrorDocument': {
            'Key': 'error.html'
            },
            'IndexDocument':{
                'Suffix': 'index.html'
            }})
    return

    #---Error Handling---#
    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration ={'LocationConstraint':session.region_name})
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket =s3.Bucket(bucket)
        else:
            raise e


#---Url of s3 websites using format strings %s---#
#url = "http://%s.s3-website.us-east2.amazonaws.com"% new_bucket.name

#---Upload file to s3 with extra arguments---#
#s3.Bucket('004-autoaws-ecparas').upload_file('01-webotron/index.html', 'index.html', ExtraArgs ={'ContentType': 'text/html'})


#---S3 Sync---#

#---python---#
#---example code: webotron sync kitten_web kittens.automatingaws.net---#
pathname = "kitten_web"
path = Path(pathname)
path.resolve()         #-shows full path-#


#---sample function---#
def handle_directory(target):
  for p in target.iterdir():
    if p.is_dir(): handle_directory(p) #-recursive calls itself
    if p.is_file(): print(p)


#---cli group option 4---#
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
def sync(pathname):
    """Sync contents of PATHNAME to BUCKET"""
    #s3_bucket =s3.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir(): handle_directory(p)
            if p.is_file(): upload_file(s3_bucket, str(p), str(p.relative_to(root)))

    handle_directory(root) #---alignment matters---#

if __name__=='__main__':
    cli()                #-call the click group-

#---NOTES---#
#import sys           #-access arguments, not needed with click module

#---Terminal Python Commands---------#
#pipenv shell
#python /webotron/webotron2020.py
#pipenv install click
#python webotron/webotron.py --help   (generate help msgs via click module)
#python webotron/webotron2020.py list-buckets
#print(policy)
#handle_directory(path)
#handle_directory(path.expanduser())---> expands tilde directory reference
