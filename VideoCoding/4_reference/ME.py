#!/usr/bin/env python

from utlis import BlockMatching
import numpy as np
import cv2
import time

FONT = cv2.FONT_HERSHEY_SIMPLEX
BLUE = (255,0,0) 
GREEN= (0,255,0)
RED  = (0,0,255)

dfd=1 ; blockSize=(16,16); searchRange=15 ; predict_from_prev = False ; N=5 

bm = BlockMatching(dfd=dfd,
            blockSize=blockSize,
            searchRange=searchRange,
            motionIntensity=False)

dfd = "MSE" if dfd else "MAD"
method = "ThreeStep"
text = ["Block Matching Algorithm","DFD: {} | {} | {} Search Range: {}".format(
    dfd,blockSize,method,searchRange)]

def visualize(prev,target,motionField,prevP,text,a,t):
    h = 70 ; w = 10
    H,W = prev.shape
    HH,WW = h+2*H+20, 2*(W+w)
    frame = np.ones((HH,WW), dtype="uint8")*255

    cv2.putText(frame, text[0], (w, 23), FONT, 0.5, 0, 1)
    cv2.putText(frame, text[1], (w, 40), FONT, 0.4, 0, 1)
    cv2.line(frame, (w, 46), (WW-w, 46),0)

    cv2.putText(frame, f"prev-{a:03d}", (w, h-4), FONT, 0.4, 0, 1)
    cv2.putText(frame, f"target-{t:03d}", (w+W, h-4), FONT, 0.4, 0, 1)
    cv2.putText(frame, "motion field", (w, h+2*H+10), FONT, 0.4, 0, 1)
    cv2.putText(frame, "predicted prev", (w+W, h+2*H+10), FONT, 0.4, 0, 1)

    frame[h:h+H, w:w+W] = prev 
    frame[h:h+H, w+W:w+2*W] = target 
    frame[h+H:h+2*H, w:w+W] = motionField 
    frame[h+H:h+2*H, w+W:w+2*W] = prevP

    return frame

print("Start Demo!")
a = 99; t = 100

start_time = time.time()

akiyo96 = cv2.imread('akiyo_96.png',0)
akiyo97 = cv2.imread('akiyo_97.png',0)
akiyo98 = cv2.imread('akiyo_98.png',0)
akiyo99 = cv2.imread('akiyo_99.png',0)
frames_prev = [akiyo96, akiyo97, akiyo98, akiyo99]
target = cv2.imread('akiyo_100.png',0)

bm.step(frames_prev,target)
prevP = bm.prevP

motionField = bm.motionField
out = visualize(akiyo98,target,motionField,prevP,text,a,t)
elapsed_time = time.time() - start_time
# print(f"Elapsed time: {elapsed_time:.3f} secs")
cv2.imshow("Demo",out)
cv2.waitKey(0)
cv2.destroyAllWindows()