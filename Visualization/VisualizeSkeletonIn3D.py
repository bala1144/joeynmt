import h5py
import numpy as np
import os
from Utils.ObjHelper import writeObj
from Utils.Commonutils import createDirectory


def SkeletonObjGenerator():
    unNormalizedSkeletonFile = '/mnt/korhal_home/masterThesis/wordAreGlosses/wacv2020/data/demo/keypoints/PHOENIX-2014-T-01-dev_filter_10.h5'
    NormalizedSkeletonFile = '/mnt/korhal_home/masterThesis/wordAreGlosses/wacv2020/data/demo/keypoints/PHOENIX-2014-T-01-dev_normalized_10.h5'
    ObjOutPath = '/home/thambiraja/myProjects/PHOENIX-2014-T/features/Lifted_Joint_obj/dev/'

    unNormalizedIn = h5py.File(unNormalizedSkeletonFile, "r")
    NormalizedIn = h5py.File(NormalizedSkeletonFile, "r")
    for key in unNormalizedIn:
        print("")
        print("... processing '%s'" % key)
        print("")
        UnNormSkel = np.array(unNormalizedIn.get(key)).reshape(-1,50,3)
        NormSkel = np.array(NormalizedIn.get(key)).reshape(-1,50,3)
        curr_Dir = os.path.join(ObjOutPath,key)
        createDirectory(curr_Dir)

        # iterate through the frames to generate
        for i in range(NormSkel.shape[0]):
            UnNormObjFile = os.path.join(curr_Dir, '%04d_UnNormalized.obj'%i)
            NormObjFile = os.path.join(curr_Dir, '%04d_.Normalized.obj'%i)
            writeObj(UnNormObjFile, UnNormSkel[i])
            writeObj(NormObjFile, NormSkel[i])

if __name__ == "__main__":
    print('Skeleten3DVisualizer')
    SkeletonObjGenerator()