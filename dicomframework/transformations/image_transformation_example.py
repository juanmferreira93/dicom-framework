from dicomframework.transformations.image_transformation import ImageTransformation


class ImageTransformationExample(ImageTransformation):
    def transform(self, images):
        # El codigo de la transformacion, lo define el usuario en la clase hija
        pass

    def transformation_name(self):
        return "image_transformation_example"
