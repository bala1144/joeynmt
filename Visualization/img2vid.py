from moviepy.editor import *
import glob
import os

def img2Vid(fileIn,outFile):
    files = glob.glob(os.path.join(fileIn, '*.png'))
    files.sort()
    clips = [ImageClip(m).set_duration(0.5) for m in files]
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(outFile, fps=50)
    return clips

def combineVideos(vid1, vid2, outfold):
    clip1 = VideoFileClip(vid1).margin(10)  # add 10px contour
    clip2 = VideoFileClip(vid2).margin(10)
    final_clip = clips_array([[clip1, clip2]])
    final_clip.write_videofile(os.path.join(outfold,"CombinedVideo.mp4"))

def combine3Videos(vid1, vid2, vid3, outfold, outVidName="CombinedVideo.mp4"):
    clip1 = VideoFileClip(vid1).margin(10)  # add 10px contour
    clip2 = VideoFileClip(vid2).margin(10)
    clip3 = VideoFileClip(vid3).margin(10)
    final_clip = clips_array([[clip1, clip2,clip3]])
    final_clip.write_videofile(os.path.join(outfold,outVidName))

def createDirectory(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def generateCompareVid():

    LiftVidDir='/home/thambiraja/myProjects/PHOENIX-2014-T/features/Vis_Lifted_3DJOints/dev/'
    outVidRoot='/home/thambiraja/myProjects/PHOENIX-2014-T/features/Lifted_Joint_Vid/dev/'
    sourceDir='/home/thambiraja/myProjects/PHOENIX-2014-T/features/fullFrame-210x260px/dev/'


    # generate the lifted joints video
    # curr_dir='01April_2010_Thursday_heute-6697'
    for root, dnames, fnames in os.walk(LiftVidDir):
        break

    for curr_dir in dnames:
        if '_topView' not in curr_dir:
            outVidDir= os.path.join(outVidRoot, curr_dir)
            createDirectory(outVidDir)

            # generate video for normalized skeleton
            vid1=os.path.join(outVidDir, "liftedClip.mp4")
            clip1 = img2Vid(os.path.join(LiftVidDir,curr_dir),vid1)

            # generate lifted video top view
            vid2=os.path.join(outVidDir, "liftedClipTopView.mp4")
            clip2 = img2Vid(os.path.join(LiftVidDir,curr_dir+"_topView"),vid2)

            # generate source video
            source_vid=os.path.join(outVidDir, "source.mp4")
            clip3 = img2Vid(os.path.join(sourceDir,curr_dir), source_vid)

            # combine videos
            combine3Videos(vid1, vid2, source_vid, outVidDir)


def compareNormalizedandUnNormalzieSkeleton():
    unNormalizedSkelDir='/home/thambiraja/myProjects/PHOENIX-2014-T/features/Vis_Lifted_3DJOints/dev/'
    NormalizedSkelDir='/home/thambiraja/myProjects/PHOENIX-2014-T/features/Lifted_Normalized_Joints/dev/'
    outVidRoot = '/home/thambiraja/myProjects/PHOENIX-2014-T/features/Lifted_Joint_Vid/dev/'

    for root, dnames, fnames in os.walk(unNormalizedSkelDir):
        break

    for curr_dir in dnames:
        if '_topView' not in curr_dir:
            outVidDir= os.path.join(outVidRoot, curr_dir)
            createDirectory(outVidDir)

            # generate video for the normalized skeletons
            vid1=os.path.join(outVidDir, "normalizedliftedClip.mp4")
            clip1 = img2Vid(os.path.join(NormalizedSkelDir,curr_dir),vid1)

            # use the pre-generated video for the unNormalized joints
            vid2=os.path.join(outVidDir, "liftedClip.mp4")
            source_vid=os.path.join(outVidDir, "source.mp4")

            # combine videos
            combine3Videos(vid2, vid1, source_vid, outVidDir, outVidName="CompareNormandUnnormJoints.mp4")


if __name__=="__main__":
    print("img 2 vid using movie py")
    # generateCompareVid()
    compareNormalizedandUnNormalzieSkeleton()
