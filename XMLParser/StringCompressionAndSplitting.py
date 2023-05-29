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
                if counter > 1:
                    degrees = 1
                    if input[i] == "c" or input[i] == "w":
                        degrees = 45
                    compressed += str(counter * degrees)
                compressed += input[i]
                counter = 1
        compressed += input[-1]

        return compressed

    @staticmethod
    def splitString(string):

        splitted = []
        for i in range((len(string)//50) + 1):

            sub = string[i*50:(i+1)*50]
            splitted.append(sub)

        return splitted

    @staticmethod
    def compressAndSplit(string):

        return StringCompressionAndSplitting.splitString(StringCompressionAndSplitting.compressString(string))

