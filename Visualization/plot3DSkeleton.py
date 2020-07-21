import h5py
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os


class VisulizeSkeleton():

    def __init__(self):
        BonePairs = np.asarray([
            0, 1,
            1, 2,
            2, 3,
            3, 4,
            1, 5,
            5, 6,
            6, 7,

            7, 8,

            8, 9,
            9, 10,
            10, 11,
            11, 12,

            8, 13,
            13, 14,
            14, 15,
            15, 16,

            8, 17,
            17, 18,
            18, 19,
            19, 20,

            8, 21,
            21, 22,
            22, 23,
            23, 24,

            8, 25,
            25, 26,
            26, 27,
            27, 28,

            4, 29,
            29, 30,
            30, 31,
            31, 32,
            32, 33,
            29, 34,
            34, 35,
            35, 36,
            36, 37,
            29, 38,
            38, 39,
            39, 40,
            40, 41,
            29, 42,
            42, 43,
            43, 44,
            44, 45,
            29, 46,
            46, 47,
            47, 48,
            48, 49])
        self.BonePairs = BonePairs.reshape(-1, 2)

    def plot3Dlines(self, XYZ,ax):
        # Iterate over each point, and plot the line.
        for Bone in self.BonePairs:
            ax.plot3D([XYZ[Bone[0], 0], XYZ[Bone[1], 0]], [XYZ[Bone[0], 1], XYZ[Bone[1], 1]], [XYZ[Bone[0], 2], XYZ[Bone[1], 2]], 'b')

    def plot3DPoints(self, XYZ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(elev=-90.0, azim=-90.0)
        ax.scatter(XYZ[:,0], XYZ[:,1], XYZ[:,2], c='r', marker='o')
        # draw bones
        self.plot3Dlines(XYZ,ax)
        plt.axis('off')
        plt.grid(b=None)
        plt.savefig(os.path.join(self.out_dir,"frame%03d.png"%self.frame))
        # plt.show()
        plt.close()

    def plot3DPoints_topView(self, XYZ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(elev=-0.0, azim=-90.0)
        ax.scatter(XYZ[:, 0], XYZ[:, 1], XYZ[:, 2], c='r', marker='o')
        # draw bones
        self.plot3Dlines(XYZ, ax)
        plt.axis('off')
        plt.grid(b=None)
        plt.savefig(os.path.join(self.out_dir_topView, "frame%03d.png" % self.frame))
        # plt.show()
        plt.close()

    def createDirectory(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def load_processed_hdf5_files(self):
        fnameIn = '/home/thambiraja/myProjects/PHOENIX-2014-T/processedData/dev/PHOENIX-2014-T-01-dev_10_filtered.h5'
        # fnameIn = '/mnt/korhal_home/masterThesis/wordAreGlosses/wacv2020/data/demo/keypoints/PHOENIX-2014-T-01-dev_filter_10.h5'
        # fnameIn = '/mnt/korhal_home/masterThesis/wordAreGlosses/wacv2020/data/demo/keypoints/PHOENIX-2014-T-01-dev_normalized_10.h5'
        outrootFolder = '/home/thambiraja/myProjects/PHOENIX-2014-T/features/Vis_Lifted_3DJOints/dev/'

        hfIn = h5py.File(fnameIn, "r")
        for key in hfIn:
            print("")
            print("... processing '%s'" % key)
            print("")

            # create output directory
            self.out_dir=os.path.join(outrootFolder, key)
            self.createDirectory(self.out_dir)

            self.out_dir_topView=os.path.join(outrootFolder, key+"_topView")
            self.createDirectory(self.out_dir_topView)

            xyz_seq = np.array(hfIn.get(key))
            for i in range(xyz_seq.shape[0]):
                print('frame ', i)
                self.frame=i
                self.plot3DPoints(xyz_seq[i].reshape(-1,3))
                self.plot3DPoints_topView(xyz_seq[i].reshape(-1,3))

            print()

if __name__ == "__main__":
    print("plot3Dpoints")
    SkelVizualizer = VisulizeSkeleton()
    SkelVizualizer.load_processed_hdf5_files()



