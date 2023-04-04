from DataGenerator.splines_generator import data_gen
from DataGenerator.splines_generator import simple_spline

def main():

    data = data_gen( 5, 5, 1280, 720)
    data.splines_generator()

if __name__ == '__main__':
    main()