from enum_motion import Motions
teststring = "rrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrr"
class StringCompressionAndSplitting():

    @staticmethod
    def compressString(string):
        input = string
        compressed = ""
        counter = 1

        for i in range(len(input) - 1):
            if input[i] == input[i+1]:
                counter += 1
            else:
                degrees = 1
                if input[i] == "c" or input[i] == "w":  # noch anpassen, da bei counter < 1 dies nicht passiert
                    degrees = 1 # da StepSize = 45

                if counter * degrees > 1:

                    compressed += str(counter * degrees)
                compressed += input[i]
                counter = 1
        compressed += input[-1]

        return compressed

    @staticmethod
    def splitString(string):

        split = []
        for i in range((len(string)//50) + 1):

            sub = string[i*50:(i+1)*50]
            split.append(sub)

        return split

    @staticmethod
    def compressAndSplit(string):

        return StringCompressionAndSplitting.splitString(StringCompressionAndSplitting.compressString(string))

