from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

# Returns EAR given eye landmarks
def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])

    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = np.linalg.norm(eye[0] - eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # Return the eye aspect ratio
    return ear

# Returns MAR given eye landmarks
def mouth_aspect_ratio(mouth):
    # Compute the euclidean distances between the three sets
    # of vertical mouth landmarks (x, y)-coordinates
    A = np.linalg.norm(mouth[13] - mouth[19])
    B = np.linalg.norm(mouth[14] - mouth[18])
    C = np.linalg.norm(mouth[15] - mouth[17])

    # Compute the euclidean distance between the horizontal
    # mouth landmarks (x, y)-coordinates
    D = np.linalg.norm(mouth[12] - mouth[16])

    # Compute the mouth aspect ratio
    mar = (A + B + C) / (2 * D)

    # Return the mouth aspect ratio
    return mar


eye_thresh = 0.3
eye_consec_frames = 50
mouth_thresh = 0.6
mouth_consec_frames = 50

eye_count = 0
mouth_count = 0
yawn_alarm = False
sleep_alarm = False

WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)

w, h = 60, 35

shape_predictor = "model/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Grab the indexes of the facial landmarks for the left and right eye and mouth respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

cap = cv2.VideoCapture(0)

while True:

	_,frame = cap.read()
	frame = imutils.resize(frame, width = 480)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	rects = detector(gray)
	if len(rects) > 0:
		rect = rects[0]
	else:
		cv2.imshow("Drowsiness Detection System", frame)
		key = cv2.waitKey(1) & 0xFF
		continue

	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)

	mouth = shape[mStart:mEnd]
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]

	mar = mouth_aspect_ratio(mouth)
	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)
	ear = (leftEAR + rightEAR) / 2.0
	diff_ear = np.abs(leftEAR - rightEAR)

	mouthHull = cv2.convexHull(mouth)
	leftEyeHull = cv2.convexHull(leftEye)
	rightEyeHull = cv2.convexHull(rightEye)
	cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
	cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
	cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)

	for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
		cv2.circle(frame, (x, y), 2, GREEN_COLOR, -1)

	if ear < eye_thresh:
		eye_count +=1
		if eye_count > eye_consec_frames:
			if not sleep_alarm:
				sleep_alarm = True

		cv2.putText(frame, "You are Sleepy!!!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	else:
	    eye_count = 0
	    sleep_alarm = False

	if mar > mouth_thresh:
		mouth_count += 1
		if mouth_count > mouth_consec_frames:
			if not yawn_alarm:
				yawn_alarm = True

		cv2.putText(frame, "You are Yawning!!!", (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	else:
		mouth_count = 0
		yawn_alarm = False

	cv2.imshow("Drowsiness Detection System", frame)
	key = cv2.waitKey(1) & 0xFF

	# If the `Esc` key was pressed, break from the loop
	if key == 27:
		break

# Do a bit of cleanup
cv2.destroyAllWindows()
cap.release()
