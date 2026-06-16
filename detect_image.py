from ultralytics import YOLO

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Run detection on image
results = model("test_phone.jpg", show=True)

# Print detected objects
for result in results:

    for box in result.boxes:

        class_id = int(box.cls[0])

        confidence = float(box.conf[0])

        object_name = model.names[class_id]

        print(f"{object_name} : {confidence:.2f}")