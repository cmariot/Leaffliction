PYTHON=python3

IMAGES_DIR="images"
SMALL_DIR="microdb"
IMAGE_TEST="image.jpg"

analysis:
	@($(PYTHON) srcs/Distribution.py $(IMAGES_DIR))

augmentation:
	@($(PYTHON) srcs/Augmentation.py $(IMAGE_TEST))

transformation:
	@($(PYTHON) srcs/Transformation.py $(IMAGE_TEST))

train:
	@(rm -rf $(SMALL_DIR)_augmented $(SMALL_DIR)_transformed)
	@($(PYTHON) srcs/train.py $(SMALL_DIR))

predict:
	@($(PYTHON) srcs/predict.py --image_path $(IMAGE_TEST))

clean:
	rm -rf */*/__pycache__


# Dependencies

requirements:
	pip freeze > requirements.txt

install_requirements:
	pip install -r requirements.txt



.PHONY: all analysis augmentation transformation classification train predict clean requirements install_requirements
