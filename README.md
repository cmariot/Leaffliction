# Leaffliction

Leaffliction is a computer vision project that aims to detect plant diseases from images.

## Part I : Data analysis

Our dataset is composed of 7,221 images of healthy and diseased leaves.
</br>
The images are divided into 8 categories, each corresponding to a different plant species or a different disease.
</br>
</br>
<img src="./utils/different_categories.png" />

## Part II : Data augmentation

But the dataset is not balanced, so we need to augment it to have the same number of images for each category.
We generate new images by applying small random transformations to the original images.
This reduces overfitting and improves the performance of our model.

## Part III : Image transformation