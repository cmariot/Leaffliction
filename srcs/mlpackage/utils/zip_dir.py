import os
import zipfile


def zip_dir(model_path, trans_dir, output_filename):

    with zipfile.ZipFile(
        output_filename, 'w', zipfile.ZIP_DEFLATED
    ) as zip_file:

        for directory in [model_path, trans_dir]:

            if not os.path.exists(directory):
                continue

            for root, _, files in os.walk(directory):
                for file in files:

                    zip_file.write(
                        os.path.join(root, file),
                    )
