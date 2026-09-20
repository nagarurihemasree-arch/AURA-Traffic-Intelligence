from ultralytics import YOLO
import os

# Load trained model
model_path = os.path.join(
    os.path.dirname(__file__),
    "best.pt"
)

model = YOLO(model_path)


def detect_issue(image_path):
    results = model(image_path, conf=0.25)

    detections = []
    annotated_image = None

    for result in results:

        # Create image with bounding boxes
        annotated_image = result.plot()

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            detections.append({
                "problem": class_name,
                "confidence": round(confidence, 2)
            })

    # Calculate severity
    if len(detections) == 0:
        severity = "Low"
    elif len(detections) == 1:
        severity = "Medium"
    else:
        severity = "High"

    return {
        "detections": detections,
        "count": len(detections),
        "severity": severity,
        "annotated_image": annotated_image
    }


# Test
if __name__ == "__main__":

    image = "../test/images/img-104_jpg.rf.7f5a44e182a85aa8e94a769c8160d443.jpg"

    result = detect_issue(image)

    print("\n--- City Early Warning Result ---")

    print("Number of problems:", result["count"])
    print("Severity:", result["severity"])

    for item in result["detections"]:
        print(
            f"Problem: {item['problem']} | "
            f"Confidence: {item['confidence']}"
        )