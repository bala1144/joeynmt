import torch

def readObj(file, device='cpu'):
    lines = open(file, 'r')
    vertices = []
    faces = []
    for line in lines:
        if 'v' in line:
            vertices.append(list(map(float, line.split()[1:])))
        if 'f' in line:
            faces.append(list(map(int, line.split()[1:])))
    vertices = torch.tensor(vertices, dtype=torch.float32, device=device)
    if faces:
        faces = torch.tensor(faces, dtype=torch.int32, device=device)
        faces = faces - 1

    return vertices, faces


def writeObj(file_name, vertices, faces=None):
    f = open(file_name, "w")
    for x in vertices:
        f.write("v {} {} {}\n".format(x[0], x[1], x[2]))

    # write faces
    if faces is not None:
        for x in faces:
            f.write("f {} {} {}\n".format(x[0]+1, x[1]+1, x[2]+1))


    f.close()