#!/usr/bin/python         //which interpreter to use
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS"""  # -denote docstrings with 3x quotes

# ---Import modules---#

import boto3
from botocore.exceptions import ClientError
import click
from botocore.exceptions import ClientError
from bucket import BucketManager

# ---Establish Session---#
session = boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)


# ---CLICK commands---#
@click.group()             # -creates a menu of available commands-#
def cli():                 # -group name = cli-#
    """Webotron deploys websites to AWS"""
    pass                   # -do nothing-#

# ---cli group option 1---#
@cli.command('list-buckets')         # -DECORATOR wraps a function-#
def list_buckets():                  # -DOCSTRING-#
    """Description: List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)

# ---cli group option 2---#
@cli.command('list-bucket-objects')
@click.argument('bucket')            # -user input via argument click feature-#
def list_bucket_objects(bucket):
    """List more crap"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)

# ---cli group option 3---#
@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure new S3 bucket"""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)



    # ---Error Handling---#



# ---Url of s3 websites using format strings %s---#
# url = "http://%s.s3-website.us-east2.amazonaws.com"% new_bucket.name

# ---Upload file to s3 with extra arguments---#
# s3.Bucket('004-autoaws-ecparas').upload_file('01-webotron/index.html', 'index.html', ExtraArgs ={'ContentType': 'text/html'})


# ---S3 Sync---#

# ---python---#
# ---example code: webotron sync kitten_web kittens.automatingaws.net---#
pathname = "kitten_web"
path = Path(pathname)
path.resolve()         #-shows full path-#


#---sample function---#
def handle_directory(target):
  for p in target.iterdir():
    if p.is_dir(): handle_directory(p) #-recursive calls itself
    if p.is_file(): print(p)


# ---cli group option 4---#
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(self, pathname, bucket_name):
    """Sync contents of PATHNAME to BUCKET"""
    bucket =self.s3.Bucket(bucket)
    bucket_manager.sync(pathname, bucket)


if __name__=='__main__':
    cli()                # -call the click group-

# ---NOTES---#
# import sys           #-access arguments, not needed with click module

# ---Terminal Python Commands---------#
# pipenv shell
# python /webotron/webotron2020.py
# pipenv install click
# python webotron/webotron.py --help   (generate help msgs via click module)
# python webotron/webotron2020.py list-buckets
# print(policy)
# handle_directory(path)
# handle_directory(path.expanduser())---> expands tilde directory reference
# code in a file is treated as a single module
# when code is run as a script, python calls it 'main'
# if module is imported, python doesn't call it 'main'
# a package is a directory of modules and other stuff
# __init__.py don't forget the dot!
# oeYQtmxgHmVFoDTGcMz2heralDuVCjvCMJ0Psoa0v68K --- #
# --AKIA46JZYZheraTNNZ2O3L7O---#
