
import numpy as np

def parse_obj(path):

    vertices=[]
    faces=[]

    f = open(path, "r")

    f1 = f.readlines()

    for line in f1:
        if(line[0] == "v"):
            vertices.append(tuple([float(i) for i in line[1:].split()]))
        if(line[0] == "f"):
            faces.append(tuple(int(i) for i in line[1:].split()))

    f.close()

    return vertices, faces
