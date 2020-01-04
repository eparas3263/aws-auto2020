#!/usr/bin/python         //which interpreter to use
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS"""  # -denote docstrings with 3x quotes

# ---Import modules---#

import boto3
import click
from bucket import BucketManager    # ---from bucket.py --- #

# ---Establish Session---#
session = boto3.Session(profile_name='pythonAWSauto')
bucket_manager = BucketManager(session)  # ---captures s3 session --- #swee


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



# ---cli group option 4---#
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET"""
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
