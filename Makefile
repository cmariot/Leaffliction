PYTHON=python3

all: analysis augmentation transformation classification

analysis:
	@(cd ./analysis ; $(PYTHON) Distribution.py ../images/)

augmentation:
	@(cd ./augmentation ; $(PYTHON) Augmentation.py ../images/Apple_healthy/image\ \(1\).JPG)

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
