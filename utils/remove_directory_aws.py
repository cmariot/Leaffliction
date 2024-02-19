import os
import s3fs

if __name__ == '__main__':

    """
    Remove a directory from a S3 bucket
    """

    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]

    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    BUCKET = "cmariot"
    DIR = "images_augmented"

    if not fs.exists(BUCKET):
        print(f"The bucket {BUCKET} does not exist.")
        exit(1)

    if not fs.exists(BUCKET + "/" + DIR):
        print(f"The directory {BUCKET}/{DIR} does not exist.")
        exit(1)

    # Remove the directory
    fs.rm(BUCKET + "/" + DIR, recursive=True)
    print(f"The directory {BUCKET}/{DIR} has been removed.")
