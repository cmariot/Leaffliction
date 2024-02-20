import os
import s3fs


if __name__ == '__main__':

    """
    Upload local files to a S3 bucket
    """

    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]

    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    BUCKET = "cmariot"
    DIR = "minifitrans"

    # If the bucket does not exist, it will be created
    if not fs.exists(BUCKET):
        print(f"{BUCKET} directory has been created.")
        fs.makedirs(BUCKET)

    if not fs.exists(BUCKET + "/" + DIR):
        print(f"{BUCKET}/{DIR} directory has been created.")
        fs.makedirs(BUCKET + "/" + DIR)

    # Walk through the directory and upload all files
    for root, dirs, files in os.walk(DIR):

        for dir in dirs:
            if not fs.exists(f"{BUCKET}/{root}/{dir}"):
                print(f"{BUCKET}/{root}/{dir} has been created.")
                fs.makedirs(f"{BUCKET}/{root}/{dir}")

        for file in files:
            print(f"{root}/{file} has been pushed to {BUCKET}/{root}/{file}")
            fs.put(f"{root}/{file}", f"{BUCKET}/{root}/{file}")
