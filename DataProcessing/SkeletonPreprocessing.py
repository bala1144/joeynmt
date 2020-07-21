import h5py
import numpy as np

class SkeletonPreprocessing():
    def __init__(self):

        refnameIn = '/home/thambiraja/myProjects/PHOENIX-2014-T/processedData/dev/PHOENIX-2014-T-01-refSeq_filtered.h5'
        ref_Frame = 19
        hfIn = h5py.File(refnameIn, "r")
        for key in hfIn:
            print("")
            print("... Setting reference Frame '%s'" % key)
            print("")
            x = np.array(hfIn.get(key)).reshape(-1, 50, 3)
            self.referenceSkeleton = x[ref_Frame]

        # choose and fix a reference skeleton
        # self.referenceSkeleton=None
        self.refShoulderDist=None
        self.ShoulderJointID={'left':2,'right':5}

        if self.referenceSkeleton is not None:
            print('Find the shoulder distance')
        # todo : need to fix the reference skeleton later

    def broadCastTranslation(self,a, b):
        c = np.zeros(a.shape)
        for i in range(c.shape[0]):
            c[i] = a[i] + b[i]
        return c

    def alignSkeleton(self, skel_seq):
        # if self.referenceSkeleton is None:
        #     self.referenceSkeleton = skel_seq[0]

        # find the translation and align the skeleton
        translation = skel_seq[:,1] - self.referenceSkeleton[1]
        alignedSeq=self.broadCastTranslation(skel_seq, translation)
        return alignedSeq

    def normalizeSkeleton(self, alignedSeq):
        if self.refShoulderDist is None:
            self.refShoulderDist = np.linalg.norm(self.referenceSkeleton[self.ShoulderJointID['left']] - self.referenceSkeleton[self.ShoulderJointID['right']])

        shoulderDistSeq=np.linalg.norm(alignedSeq[:, self.ShoulderJointID['left']] - alignedSeq[:, self.ShoulderJointID['right']], axis=1)
        scale = self.refShoulderDist / shoulderDistSeq

        # normalize the skeletons
        refNeckJoint = self.referenceSkeleton[1]
        normalizedSkelSeq = np.zeros(alignedSeq.shape)
        for i in range(normalizedSkelSeq.shape[0]):
            normalizedSkelSeq[i] = refNeckJoint + (alignedSeq[i, :] - refNeckJoint) * scale[i]

        return normalizedSkelSeq


    def preProcessSkeleton(self, fnameIn=None):
        fnameIn = '/mnt/korhal_home/masterThesis/wordAreGlosses/wacv2020/data/demo/keypoints/PHOENIX-2014-T-01-dev_filter_10.h5'
        fnameOut = '/mnt/korhal_home/masterThesis/wordAreGlosses/wacv2020/data/demo/keypoints/PHOENIX-2014-T-01-dev_normalized_10.h5'

        hfIn = h5py.File(fnameIn, "r")
        hfOut = h5py.File(fnameOut, "w")
        for key in hfIn:
            print("")
            print("... processing '%s'" % key)
            print("")
            x = np.array(hfIn.get(key)).reshape(-1,50,3)
            alignedSeq = self.alignSkeleton(x)
            normalizedSkelSeq = self.normalizeSkeleton(alignedSeq)
            hfOut.create_dataset(key, data=normalizedSkelSeq, dtype=normalizedSkelSeq.dtype)


if __name__ == "__main__":
    print('skeletonProcessing')
    skel_ppr = SkeletonPreprocessing()
    skel_ppr.preProcessSkeleton()