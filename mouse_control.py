import cv2
import mediapipe as mp
import pyautogui

capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)

x1 = y1 = x2 = y2 = 0
control_mode = "file_open"

# Smoothing parameters
alpha = 0.3
smoothed_mouse_x = smoothed_mouse_y = 0

while True:
    _, image = camera.read()
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == 8:
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)

                    # Apply smoothing to mouse movement
                    smoothed_mouse_x = alpha * smoothed_mouse_x + (1 - alpha) * mouse_x
                    smoothed_mouse_y = alpha * smoothed_mouse_y + (1 - alpha) * mouse_y

                    cv2.circle(image, (x, y), 10, (0, 255, 255))
                    pyautogui.moveTo(int(smoothed_mouse_x), int(smoothed_mouse_y))
                    x1 = x
                    y1 = y

                if id == 4:
                    x2 = x
                    y2 = y
                    cv2.circle(image, (x, y), 10, (0, 255, 255))

                if id == 12 and x < x1:
                    control_mode = "volume"
                elif id == 20 and x > x1:
                    control_mode = "file_open"

        dist = y2 - y1
        print(dist)

        if control_mode == "file_open" and dist < 20:
            pyautogui.click()

        elif control_mode == "volume":
            dist_volume = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
            print(dist_volume)
            if dist_volume > 50:
                pyautogui.press("Volumeup")
            else:
                pyautogui.press("Volumedown")

    cv2.imshow("Combined Hand Gesture", image)
    key = cv2.waitKey(10)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
 