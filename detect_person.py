
from pathlib import Path
import json
import csv
import cv2
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
OUTPUT_DIR = BASE_DIR / "outputs"

DISASTER_TYPES = ["earthquake", "flood", "cyclone"]

# Experimental settings to help detect smaller people
CONFIDENCE = 0.15
IMAGE_SIZE = 960


def main():
    print("Loading pretrained YOLO model...")
    model = YOLO("yolo26n.pt")

    total_images = 0
    total_candidates = 0

    for disaster in DISASTER_TYPES:
        image_dir = DATASET_DIR / disaster / "images"
        labels_dir = DATASET_DIR / disaster / "labeled"
        output_dir = OUTPUT_DIR / disaster

        output_dir.mkdir(parents=True, exist_ok=True)

        if not image_dir.exists():
            print(f"Missing folder: {image_dir}")
            continue

        images = sorted(
            p for p in image_dir.iterdir()
            if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
        )

        if not images:
            print(f"No images found in {image_dir}")
            continue

        print(f"\n{'=' * 45}")
        print(f"Disaster type: {disaster.upper()}")
        print(f"Images found: {len(images)}")
        print("=" * 45)

        all_detections = []
        image_checklist = []

        for image_path in images:
            result = model.predict(
                source=str(image_path),
                classes=[0],
                conf=CONFIDENCE,
                imgsz=IMAGE_SIZE,
                verbose=False
            )[0]

            height, width = result.orig_shape
            boxes = result.boxes
            count = len(boxes) if boxes is not None else 0

            annotated_path = (
                output_dir / f"{image_path.stem}_detected.jpg"
            )
            annotated_image = result.plot(
                conf=True,
                labels=True,
                line_width=1,
                font_size=8,
                pil=False
            )
            cv2.imwrite(str(annotated_path), annotated_image)

            # Check whether a corresponding annotation file exists
            label_path = labels_dir / f"{image_path.stem}.txt"
            label_exists = label_path.exists()

            # Build detection records
            if boxes is not None:
                for index, box in enumerate(boxes, start=1):
                    x1, y1, x2, y2 = [
                        int(round(v))
                        for v in box.xyxy[0].tolist()
                    ]

                    confidence = float(box.conf[0].item())

                    # Normalized coordinates (range approximately 0-1)
                    x_center = ((x1 + x2) / 2) / width
                    y_center = ((y1 + y2) / 2) / height
                    box_width = (x2 - x1) / width
                    box_height = (y2 - y1) / height

                    candidate = {
                        "candidate_id": (
                            f"{disaster.upper()}-"
                            f"{image_path.stem}-{index:03d}"
                        ),
                        "disaster_type": disaster,
                        "class_label": "person",
                        "confidence": round(confidence, 4),
                        "bounding_box_pixels": {
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2
                        },
                        "bounding_box_normalized": {
                            "x_center": round(x_center, 6),
                            "y_center": round(y_center, 6),
                            "width": round(box_width, 6),
                            "height": round(box_height, 6)
                        },
                        "image_id": image_path.name,
                        "image_width": width,
                        "image_height": height,
                        "drone_id": None,
                        "location_id": None,
                        "verification_status": "UNVERIFIED_CANDIDATE"
                    }

                    all_detections.append(candidate)

            # One checklist entry for EVERY image, even with zero detections
            checklist_entry = {
                "image_id": image_path.name,
                "disaster_type": disaster,
                "image_width": width,
                "image_height": height,
                "detected_candidates": count,
                "annotated_image_saved": annotated_path.exists(),
                "confidence_available": count > 0,
                "bounding_boxes_available": count > 0,
                "candidate_ids_generated": count > 0,
                "label_file_exists": label_exists,
                "drone_id": "NOT_PROVIDED",
                "location_id": "NOT_PROVIDED",
                "verification_status": "UNVERIFIED_CANDIDATE",
                "result": (
                    "CANDIDATES_FOUND"
                    if count > 0
                    else "NO_CANDIDATES_FOUND"
                )
            }

            image_checklist.append(checklist_entry)

            print(
                f"{image_path.name} | "
                f"Candidates: {count} | "
                f"Size: {width}x{height} | "
                f"Labels: {'Found' if label_exists else 'Missing'}"
            )

        # Save all detections for this disaster category
        detections_path = output_dir / "detections.json"
        detections_path.write_text(
            json.dumps(all_detections, indent=2),
            encoding="utf-8"
        )

        # Save detailed checklist as JSON
        checklist_json = output_dir / "image_checklist.json"
        checklist_json.write_text(
            json.dumps(image_checklist, indent=2),
            encoding="utf-8"
        )

        # Save checklist as CSV for easy viewing in Excel
        checklist_csv = output_dir / "image_checklist.csv"

        with checklist_csv.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=image_checklist[0].keys()
            )
            writer.writeheader()
            writer.writerows(image_checklist)

        category_candidates = len(all_detections)
        total_images += len(images)
        total_candidates += category_candidates

        print(f"\nImages processed: {len(images)}")
        print(f"Person candidates: {category_candidates}")
        print(f"Saved to: {output_dir}")

    print("\n" + "=" * 45)
    print("PROCESSING SUMMARY")
    print("=" * 45)
    print(f"Total images processed: {total_images}")
    print(f"Total person candidates: {total_candidates}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("Review image_checklist.csv for per-image results.")
    print("Remember: detections are unverified candidates.")


if __name__ == "__main__":
    main()
