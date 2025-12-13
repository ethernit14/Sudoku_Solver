import cv2 as cv
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2
) as hands:
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            break
        
        frame = cv.flip(frame, 1)
        
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_idx, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                hand_label = handedness.classification[0].label
                
                fingers_up = 0
                
                landmarks = hand_landmarks.landmark
                
                thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
                
                thumb_distance = abs(thumb_tip.x - thumb_mcp.x)
                
                if hand_label == "Right":
                    if thumb_tip.x < thumb_mcp.x and thumb_distance > 0.02:
                        fingers_up += 1
                else:
                    if thumb_tip.x > thumb_mcp.x and thumb_distance > 0.02:
                        fingers_up += 1
                
                finger_tips = [
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP
                ]
                finger_pips = [
                    mp_hands.HandLandmark.INDEX_FINGER_PIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                    mp_hands.HandLandmark.RING_FINGER_PIP,
                    mp_hands.HandLandmark.PINKY_PIP
                ]
                
                for tip, pip in zip(finger_tips, finger_pips):
                    if landmarks[tip].y < landmarks[pip].y:
                        fingers_up += 1
                
                h, w, c = frame.shape
                palm_x = int(landmarks[mp_hands.HandLandmark.WRIST].x * w)
                palm_y = int(landmarks[mp_hands.HandLandmark.WRIST].y * h)
                
                cv.putText(frame, f'{hand_label}: {fingers_up}', 
                          (palm_x - 50, palm_y), 
                          cv.FONT_HERSHEY_SIMPLEX, 
                          0.7, (255, 255, 255), 2)
        cv.imshow('Hand Detection', frame)
        
        # Exit on 'q' key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
