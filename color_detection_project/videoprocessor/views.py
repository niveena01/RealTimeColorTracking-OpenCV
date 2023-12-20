import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import numpy as np


def home(request):
    return render(request, 'home.html')


def get_frame():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range of blue color in HSV
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Threshold the frame to capture only the blue color
        mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        ret, jpeg = cv2.imencode('.jpg', result)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()


@gzip.gzip_page
def live_color_capture(request):
    try:
        return StreamingHttpResponse(get_frame(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass







# from django.shortcuts import render
# import cv2
# import numpy as np
#
#
# # Create your views here.

# # def ColorTracking(request):
# #     cap = cv2.VideoCapture(0)
# #     while 1:
# #         _, frame = cap.read()
# #         new_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert color to hsv color
# #         cv2.imshow('Original video', new_image)
# #
# #         lower_bound = np.array([110, 50, 50])
# #         upper_bound = np.array([120, 255, 255])
# #         # lower_bound, upper_bound = get_color_bounds(selected_color)
# #         mask = cv2.inRange(new_image, lower_bound, upper_bound)  # masking
# #         # cv2.imshow('Mask', mask)
# #
# #         res = cv2.bitwise_and(frame, frame, mask=mask)
# #         cv2.imshow('color tracking', res)
# #
# #         k = cv2.waitKey(5) & 0xFF
# #         if k == 27:
# #             break
# #
# #     cv2.destroyAllWindows()
# #
# #     return render(request, 'color_tracking_close.html')
#
# #
# # def get_color_bounds(color_name):
# #     # Define color bounds based on color name
# #     color_bounds = {
# #         'blue': (np.array([110, 50, 50]), np.array([130, 255, 255])),
# #         'red': (np.array([0, 100, 100]), np.array([10, 255, 255])),
# #         # Add more color definitions as needed
# #     }
# #     return color_bounds.get(color_name, (np.array([110, 50, 50]), np.array([130, 255, 255])))

