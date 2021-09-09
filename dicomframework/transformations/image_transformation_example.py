import numpy as np
from PIL import Image, ImageEnhance

from dicomframework.transformations.image_transformation import ImageTransformation


class ImageTransformationExample(ImageTransformation):
    def transform(self, image):
        factor = 2
        image = ImageEnhance.Contrast(image).enhance(factor)
        image = np.uint8(image)
        image = Image.fromarray(image)

        return image

    def transformation_name(self):
        return "image_transformation_example"
