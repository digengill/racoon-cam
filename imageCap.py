import cv2
vidcap = cv2.VideoCapture(0)
vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
success,image = vidcap.read()
count = 0
while success and count < 1:
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
