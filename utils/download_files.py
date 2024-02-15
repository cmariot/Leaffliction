import os
import s3fs

if __name__ == '__main__':

    """
    Download all files from a S3 bucket to a local directory
    """

    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]

    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    BUCKET = "cmariot"
    DIR = "model"

    if not fs.exists(BUCKET):
        print(f"The bucket {BUCKET} does not exist.")
        exit(1)

    if not fs.exists(BUCKET + "/" + DIR):
        print(f"The directory {BUCKET}/{DIR} does not exist.")
        exit(1)

    # Create the directory if it does not exist
    if not os.path.exists(DIR):
        os.makedirs(DIR)

    # Download recursively all files from the bucket
    for root, dirs, files in fs.walk(BUCKET + "/" + DIR):

        local_root = root.replace(BUCKET + "/" + DIR, DIR)

        for dir in dirs:
            if not os.path.exists(f"{local_root}/{dir}"):
                os.makedirs(f"{local_root}/{dir}")

        for file in files:
            print(f"{root}/{file}")
            fs.get(f"{root}/{file}", f"{root}/{file}")
