import json
import glob
import os
import numpy as np
import torch

class iterativeOptimizer():
    """
    Optimizer class for lifing the joints from 2D to 3D space for the sequence
    """
    def __init__(self):
        pass

    def formulaeProblem(self):
        pass

    def optimize(self, numFrames, numJoint=14):

        Zval = torch.zeros([numFrames, numJoint], requires_grad=True)
        optimizer = torch.optim.SGD([Zval], lr=0.01, momentum=0.9)
        # formulate the loss

        # load the joints for all the poses

    def frameWiseLoss(self, Joints2D):
        pass



class IterativeSkeletalLifiting():

    def __init__(self):
        #openPoseBonePairsString='1,8,1,2,1,5,  2,3,   3,4,   5,6,   6,7,   8,9,   9,10,  10,11, 8,12,  12,13, 13,14,  1,0,   0,15, 15,17,  0,16, 16,18,   2,17,  5,18,   14,19,19,20,14,21, 11,22,22,23,11,24'
        openPoseBonePairsString='0,1, 1,8, 1,2, 1,5,  2,3,   3,4,   5,6,   6,7,   8,9,  8,12,   0,15, 15,17,  0,16, 16,18'
        self.openPoseBonePairs=np.asarray(openPoseBonePairsString.split(",")).astype(np.int32).reshape(-1, 2)

    def read2DJointsforSeq(self, seqFolder='/home/thambiraja/Documents/PHOENIX-2014-T-release-v3/PHOENIX-2014-T/features/OpenPoseJoints/dev/01April_2010_Thursday_heute-6697', fileExt='.json'):

        # for all the file in the folder
        # read the openPose Joints from the file
        Joint2DList=[]
        leftHandKeypointsList=[]
        rightHandKeypointsList=[]

        files = glob.glob(os.path.join(seqFolder, 'images*'))
        files.sort()

        for file in files:
            with open(file) as json_file:
                data = json.load(json_file)
                joints = np.asarray(data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
                Joint2DList.append(joints[:, :2])
                leftHandKeypointsList.append(data['people'][0]['hand_left_keypoints_2d'])
                rightHandKeypointsList.append(data['people'][0]['hand_right_keypoints_2d'])

        return Joint2DList, leftHandKeypointsList, rightHandKeypointsList

    def findAvgBoneLenForSeq(self, Joint2DList):

        Joint2DList = np.asarray(Joint2DList)
        boneDiffVectors_seq = Joint2DList[:, self.openPoseBonePairs[:, 0]] - Joint2DList[:, self.openPoseBonePairs[:, 1]]
        boneLength_seq = np.linalg.norm(boneDiffVectors_seq, axis=2)
        boneLengthSeq_Avg = np.average(boneLength_seq, axis=0)

        return boneLengthSeq_Avg

    def IterativeSkletalLifting(self, boneLengthSeq_Avg):

        pass

    def computeJointVelocities(self):
        pass

    def VelocityRegularizer(self):
        pass

    def AvgBoneLenRegularizer(self):
        pass

    def StartProcess(self):

        Joint2DList, leftHandKeypointsList, rightHandKeypointsList = self.read2DJointsforSeq()

        # find the average bone length
        boneLengthSeq_Avg = self.findAvgBoneLenForSeq(Joint2DList)

        # Iterative Lifting
        self.IterativeSkletalLifting(boneLengthSeq_Avg)


if __name__ == "__main__":
    print("Iterative Skeletal Lifing")
    ISC=IterativeSkeletalLifiting()
    ISC.StartProcess()

