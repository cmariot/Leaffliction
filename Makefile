PYTHON=python3

all: analysis augmentation transformation classification

analysis:
	@(cd ./analysis ; $(PYTHON) Distribution.py)

augmentation:
	@(cd ./augmentation ; $(PYTHON) Augmentation.py)

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

.PHONY: all analysis augmentation transformation classification train predict clean
