#!/usr/bin/python         //tells user how to run Code
#-*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS"""  #-denote docstrings with 3x quotes

#---import modules---#
from pathlib import Path
import boto3
from botocore.exceptions import ClientError   #-group similar libraries together
import click
import mimetypes


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
