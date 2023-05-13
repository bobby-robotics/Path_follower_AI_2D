def motionCoordinates(path):
    u = [0, 1]
    d = [0, -1]
    l = [-1, 0]
    r = [1, 0]
    sum = [0, 0]
    pos = [[0, 0]]

    for i in path:
            match i:
                case "u": 
                    sum[0] = sum[0] + u[0]
                    sum[1] = sum[1] + u[1]
                    pos.append([sum[0], sum[1]])
                case "d": 
                    sum[0] = sum[0] + d[0]
                    sum[1] = sum[1] + d[1]
                    pos.append([sum[0], sum[1]])
                case "l": 
                    sum[0] = sum[0] + l[0]
                    sum[1] = sum[1] + l[1]
                    pos.append([sum[0], sum[1]])
                case "r": 
                    sum[0] = sum[0] + r[0]
                    sum[1] = sum[1] + r[1]
                    pos.append([sum[0], sum[1]])
                case "r,u": 
                    sum[0] = sum[0] + r[0] + u[0]
                    sum[1] = sum[1] + r[1] + u[1]
                    pos.append([sum[0], sum[1]])
                case "r,d": 
                    sum[0] = sum[0] + r[0] + d[0]
                    sum[1] = sum[1] + r[1] + d[1]
                    pos.append([sum[0], sum[1]])
                case "l,u": 
                    sum[0] = sum[0] + l[0] + u[0]
                    sum[1] = sum[1] + l[1] + u[1]
                    pos.append([sum[0], sum[1]])
                case "l,d": 
                    sum[0] = sum[0] + l[0] + d[0]
                    sum[1] = sum[1] + l[1] + d[1]
                    pos.append([sum[0], sum[1]])

    file_path = 'MotionCoordinates.txt' 

    if file_path is None:
        print('file not found')
        exit()
    else:
        with open(r'MotionCoordinates.txt', 'w') as fp:

            for items in pos:
                string1 = str(items[0])
                string2 = ','
                string3 = str(items[1])
                strings = string1 + string2 + string3 + "\n"
                fp.write(strings)
