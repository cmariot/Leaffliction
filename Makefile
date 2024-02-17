PYTHON=python3
IMAGE_DIR=microdb
IMAGE_TEST=image\ \(1\).JPG

all: analysis augmentation transformation classification

analysis:
	@($(PYTHON) srcs/Distribution.py $(IMAGE_DIR))

augmentation:
	@($(PYTHON) srcs/Augmentation.py $(IMAGE_TEST))

transformation:
	@(cd ./transformation ; $(PYTHON) Transformation.py)

classification:
	@(cd ./classification ; $(PYTHON) train.py)
	@(cd ./classification ; $(PYTHON) predict.py)

train:
	@(cd ./classification ; $(PYTHON) train.py)

predict:
	@(cd ./classification ; $(PYTHON) predict.py)

clean:
	rm -rf */*/__pycache__


# Dependencies

requirements:
	pip freeze > requirements.txt

install_requirements:
	pip install -r requirements.txt



.PHONY: all analysis augmentation transformation classification train predict clean requirements install_requirements
