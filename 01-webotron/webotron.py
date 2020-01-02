import boto3
import click
import mimetypes
from botocore.exceptions import ClientError
from pathlib import Path
# import sys


session = boto3.Session(profile_name ='pythonAutomation')
s3 = session.resource('s3')

# @click.command('list-buckets')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass
@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List more crap"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)
    pass

def upload_files(s3_bucket, path, key):
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
          'ContentType': 'text/html'
        })

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
# @click.argumnent('bucket')
def synch(pathname, bucket):
    "Sync contents of PATHNAME to BUCKET"
    s3_bucket =s3.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
      for p in target.iterdir():
        if p.is_dir(): handle_directory(p)
        if p.is_file(): upload_file(s3_bucket, str(p), str(p.relative_to(root)))


        #if p.is_file(): print("Path: {}\n Key: {}".format(p, p.relative_to(root)))

    handle_directory(root) #---alignment matters---#

if __name__=='__main__':
    cli()

    #list_buckets()
    # print(sys.argv)
    #for bucket in s3.buckets.all():
    #    print(bucket)
