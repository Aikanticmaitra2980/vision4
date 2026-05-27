import cv2 as cv
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.85, min_tracking_confidence=0.85)
mp_draw = mp.solutions.drawing_utils

# Create a blank white canvas
canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255

prev_x, prev_y = 0, 0
draw_color = (0, 0, 255) # Red
brush_thickness = 5

cap = cv.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
        
    # Resize frame to match canvas size and flip it for a mirror effect
    frame = cv.resize(frame, (640, 480))
    frame = cv.flip(frame, 1)
    h, w, c = frame.shape

    # MediaPipe processing
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw the UI Clear Button on the live frame
    cv.rectangle(frame, (20, 20), (150, 70), (200, 200, 200), cv.FILLED)
    cv.putText(frame, "CLEAR", (45, 52), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # Get Tip and Pip joint coordinates for Index and Middle fingers
            id8_x = int(hand_lms.landmark[8].x * w)
            id8_y = int(hand_lms.landmark[8].y * h)
            id12_x = int(hand_lms.landmark[12].x * w)
            id12_y = int(hand_lms.landmark[12].y * h)

            # Check if fingers are up
            index_up = hand_lms.landmark[8].y < hand_lms.landmark[6].y
            middle_up = hand_lms.landmark[12].y < hand_lms.landmark[10].y

            # 1. Selection / Hover Mode (Both fingers up)
            if index_up and middle_up:
                prev_x, prev_y = 0, 0  # Reset drawing anchor
                cv.circle(frame, (id8_x, id8_y), 15, (0, 255, 255), cv.FILLED)

                # Check if user is hovering over the CLEAR button
                if 20 < id8_x < 150 and 20 < id8_y < 70:
                    canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255
                    cv.putText(frame, "Clearing....", (230, 250), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # 2. Drawing Mode (Only Index finger up)
            elif index_up and not middle_up:
                cv.circle(frame, (id8_x, id8_y), 10, draw_color, cv.FILLED)

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = id8_x, id8_y

                # Draw onto the canvas
                cv.line(canvas, (prev_x, prev_y), (id8_x, id8_y), draw_color, brush_thickness)
                prev_x, prev_y = id8_x, id8_y
                
            else:
                prev_x, prev_y = 0, 0
    else:
        prev_x, prev_y = 0, 0

    # Advanced Blending: Overlay canvas drawings smoothly onto the webcam feed
    gray_canvas = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)
    # Create a mask where the canvas drawing exists (anything not white)
    _, mask = cv.threshold(gray_canvas, 200, 255, cv.THRESH_BINARY_INV)
    
    # Take the drawn lines from the canvas
    foreground = cv.bitwise_and(canvas, canvas, mask=mask)
    # Punch a hole in the webcam frame where the drawings will go
    background = cv.bitwise_and(frame, frame, mask=cv.bitwise_not(mask))
    
    # Merge them together
    combined_frame = cv.add(background, foreground)

    # Display Windows
    cv.imshow("Air Canvas - Live Feed", combined_frame)
    cv.imshow("Saved Artwork Canvas", canvas)

    # Press 'ESC' to exit
    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()