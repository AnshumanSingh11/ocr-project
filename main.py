
import os
import sys
from ocr import extract_text
from translate import translate_hi_to_en
from nlp_utils import simple_ner
from db import init_db, insert_record

def capture_image_from_camera(output_path):
    import cv2
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Could not access camera.")
        return None

    print("📸 Press SPACE to capture, ESC to exit.")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break
        cv2.imshow("Capture Image", frame)

        key = cv2.waitKey(1)
        if key % 256 == 27:
            print("❌ Capture cancelled.")
            cam.release()
            cv2.destroyAllWindows()
            return None
        elif key % 256 == 32:
            cv2.imwrite(output_path, frame)
            print(f"✅ Image captured and saved to {output_path}")
            break

    cam.release()
    cv2.destroyAllWindows()
    return output_path

def process_image(image_path):
    print("🔍 Performing OCR...")
    ocr_text = extract_text(image_path)
    print("📝 Extracted Text:")
    print(ocr_text)

    print("🔠 Translating to English...")
    translation = translate_hi_to_en(ocr_text)
    print("🌐 Translation:")
    print(translation)

    print("🧠 Named Entities:")
    entities = simple_ner(translation)
    print("🔹", entities)

    insert_record(ocr_text, translation, entities)
    print("✅ Done! Text stored in database.")

if __name__ == "__main__":
    init_db()
    if len(sys.argv) == 2 and sys.argv[1] == "--camera":
        image_path = "assets/captured.jpg"
        image_file = capture_image_from_camera(image_path)
        if image_file:
            process_image(image_file)
    elif len(sys.argv) == 2:
        process_image(sys.argv[1])
    else:
        print("Usage:")
        print("  python main.py <image_path>")
        print("  python main.py --camera   # to capture from webcam")
