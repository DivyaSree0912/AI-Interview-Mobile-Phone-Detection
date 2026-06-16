from ultralytics import YOLO
import cv2
import json

# Load model
model = YOLO("yolov8n.pt")

# Open video
cap = cv2.VideoCapture("video.mp4")

phone_detected = False
max_confidence = 0

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])

            confidence = float(box.conf[0])

            object_name = model.names[class_id]

            # Check if phone is detected
            if object_name == "cell phone":

                phone_detected = True

                if confidence > max_confidence:
                    max_confidence = confidence

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Phone {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

    cv2.imshow("Phone Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

if phone_detected:

    print("Suspicious Activity Detected: Mobile Phone Usage")

else:

    print("No Mobile Phone Detected")


output = {
    "phone_detected": phone_detected,
    "confidence": round(max_confidence, 2)
}

print(json.dumps(output, indent=4))