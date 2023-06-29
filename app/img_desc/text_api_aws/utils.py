import cv2
import numpy as np

def draw_ocr_results(image, text, poly, color=(0, 255, 0)):
   # unpack the bounding box, taking care to scale the coordinates
   # relative to the input image size
   (h, w) = image.shape[:2]
   tlX = int(poly[0]["X"] * w)
   tlY = int(poly[0]["Y"] * h)
   trX = int(poly[1]["X"] * w)
   trY = int(poly[1]["Y"] * h)
   brX = int(poly[2]["X"] * w)
   brY = int(poly[2]["Y"] * h)
   blX = int(poly[3]["X"] * w)
   blY = int(poly[3]["Y"] * h)
   # build a list of points and use it to construct each vertex
   # of the bounding box
   pts = ((tlX, tlY), (trX, trY), (brX, brY), (blX, blY))
   topLeft = pts[0]
   topRight = pts[1]
   bottomRight = pts[2]
   bottomLeft = pts[3]
   # draw the bounding box of the detected text
   cv2.line(image, topLeft, topRight, color, 2)
   cv2.line(image, topRight, bottomRight, color, 2)
   cv2.line(image, bottomRight, bottomLeft, color, 2)
   cv2.line(image, bottomLeft, topLeft, color, 2)
   # draw the text itself
   cv2.putText(image, text, (topLeft[0], topLeft[1] - 10),
      cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
   # return the output image
   return image
