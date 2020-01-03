#!/usr/bin/python         //which interpreter to use
# -*- coding: utf-8 -*-
import mimetypes
from pathlib import Path

"""Clases for S3 Buckets"""  # -denote docstrings with 3x quotes

class BucketManager:
    """Manage an S3 Bucket."""
    def __init__(self,session):
        """Create a BucketManager object."""
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Iterate for all objects in bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create new s3 bucket"""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration ={'LocationConstraint': self.session.region_name})
        except ClientError as e:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket)
            else:
                raise error

        return s3_bucket

    def set_policy(self, bucket):
        # ---Replace bucket with placeholder %s---#
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
            """ % bucket.name
        # ---Fix the JSON error to remove whitespace chars from string---#
        policy = policy.strip()

        # ---Create bucket policy---#
        pol = bucket.Policy()

        # ---Apply policy to objects---#
        pol.put(Policy=policy)

    def configure_website(self, bucket):

            # ---Setup website Configuration---#
            ws = bucket.Website()
            ws.put(WebsiteConfiguration={
                    'ErrorDocument': {
                    'Key': 'error.html'
                    },
                    'IndexDocument':{
                        'Suffix': 'index.html'
                    }})
            return
    @staticmethod
    def upload_file(bucket, path, key):
            content_type = mimetypes.guess_type(key)[0] or 'text/plain'
            bucket.upload_file(
                path,
                key,
                ExtraArgs={
                  'ContentType': 'text/html'
                })

    def sync(self, pathname, bucket_name):
       bucket = self.s3.Bucket(bucket)
       root = Path(pathname).expanduser().resolve()

       def handle_directory(target):
           for p in target.iterdir():
               if p.is_dir(): handle_directory(p)
               if p.is_file(): self.upload_file(s3_bucket, str(p), str(p.relative_to(root)))

       handle_directory(root)   # ---alignment matters---#
# ---TWASK--- #
# dont forget space after def!
# dont forget space after return!
