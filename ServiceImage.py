class ServiceImage:
    def read_tag(self):
        return str() if not self.tag else (':' + self.tag)

    def __init__(self, image):
        try:
            self.name, self.tag = image.split(":")
        except ValueError:
            self.name = image
            self.tag = None

    def __str__(self):
        return self.name + self.read_tag()
