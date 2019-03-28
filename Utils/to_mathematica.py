
def convert(pos, times, vels):
    opn = "= <|"
    close = "|>;"
    posStr = "pos "+opn
    timeStr = "times "+opn
    velStr = "vels "+opn

    for i in range(len(vels)):
        leg = pos[i]
        v = vels[i]
        posStr += "{0}->{{{1},{2}}}, ".format(i+1,leg[0],leg[1])
        velStr += "{0}->{{{1},{2}}}, ".format(i+1,v[0],v[1])
    for i in range(len(times)):    
        timeStr += "{0}->{1}, ".format(i+1, times[i])
    
    print(posStr[:-2]+close)
    print(timeStr[:-2]+close)
    print(velStr[:-2]+close)

