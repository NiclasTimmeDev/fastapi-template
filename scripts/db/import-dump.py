import argparse
from datetime import datetime
import subprocess

INPUT_DIR = "dumps"

parser = argparse.ArgumentParser()
parser.add_argument('--container', '-c',
                    help="The name of the docker container.")
parser.add_argument('--user', '-u', help="The database user name")
parser.add_argument('--database', '-d', help="The name of the database.")
parser.add_argument(
    '--file', '-f', help="The path to the sql file.")
args = parser.parse_args()

if not args.container or not args.user or not args.database or not args.file:
    print("Please provide values for container, user, database and filename. Type --help for more information.")
    exit(1)

subprocess.call(
    f"docker container exec {args.container} pg_restore --verbose --clean --no-acl --no-owner -U {args.user} -d {args.database} /home/{args.file}", shell=True)
