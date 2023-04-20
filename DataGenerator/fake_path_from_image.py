from Bildverarbeitung.Final.Line import Line

class fake_path_from_image():

    @staticmethod
    def create_fake_path(img, START_X_COORDINATE:int, STATE_DIMENSION:int):

        points, states = Line.states(img, 20, 5)

        return Line.show(img, points, states, scale=0.8, withpath=True)
