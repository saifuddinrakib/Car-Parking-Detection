import cv2
from src.utils import Park_classifier, Coordinate_denoter


def demonstration():
    """Demonstrates the application of parking space classification."""
    rect_width, rect_height = 107, 48
    car_park_positions_path = "data/source/CarParkPos"
    video_path = "data/source/carPark.mp4"

    classifier = Park_classifier(car_park_positions_path, rect_width, rect_height)
    coord_denoter = Coordinate_denoter(rect_width, rect_height, car_park_positions_path)

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = classifier.implement_process(frame)
        denoted_image = classifier.classify(frame, processed_frame)

        cv2.imshow("Car Park Status", denoted_image)

        cv2.setMouseCallback("Car Park Status", coord_denoter.mouseClick)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite("output.jpg", denoted_image)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    demonstration()
