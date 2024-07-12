import cv2
import pickle
import numpy as np


class Park_classifier:
    """Uses image processing methods to classify parking space occupancy."""

    def __init__(self, car_park_positions_path="data/source/CarParkPos", rect_width=None, rect_height=None):
        self.car_park_positions_path = car_park_positions_path
        self.car_park_positions = self._read_positions()
        self.rect_width = rect_width or 107
        self.rect_height = rect_height or 48

    def _read_positions(self):
        """Reads car park positions from a pickle file."""
        try:
            with open(self.car_park_positions_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error: {e}\nFailed to read car park positions file.")
            return []

    def classify(self, image: np.ndarray, processed_image: np.ndarray, threshold: int = 900) -> np.ndarray:
        """Classifies parking spaces based on processed image."""
        empty_car_park = 0
        for x, y in self.car_park_positions:
            col_start, col_stop = x, x + self.rect_width
            row_start, row_stop = y, y + self.rect_height
            crop = processed_image[row_start:row_stop, col_start:col_stop]
            count = cv2.countNonZero(crop)
            empty_car_park, color, thick = [empty_car_park + 1, (0, 255, 0), 5] if count < threshold else [
                empty_car_park, (0, 0, 255), 2]
            cv2.rectangle(image, (x, y), (x + self.rect_width, y + self.rect_height), color, thick)

        # Drawing legend rectangle
        cv2.rectangle(image, (45, 30), (250, 75), (180, 0, 180), -1)
        ratio_text = f'Free: {empty_car_park}/{len(self.car_park_positions)}'
        cv2.putText(image, ratio_text, (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        return image

    def implement_process(self, image: np.ndarray) -> np.ndarray:
        """Processes image to prepare for classification."""
        kernel_size = np.ones((3, 3), np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        Thresholded = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        blur = cv2.medianBlur(Thresholded, 5)
        dilate = cv2.dilate(blur, kernel_size, iterations=1)
        return dilate


class Coordinate_denoter:
    """Manages car park coordinate manipulation."""

    def __init__(self, rect_width=107, rect_height=48, car_park_positions_path="data/source/CarParkPos"):
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.car_park_positions_path = car_park_positions_path
        self.car_park_positions = self.read_positions()

    def read_positions(self):
        """Reads car park positions from a pickle file."""
        try:
            with open(self.car_park_positions_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error: {e}\nFailed to read car park positions file.")
            return []

    def mouseClick(self, event, x, y, flags, param):
        """Handles mouse clicks to manipulate car park positions."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.car_park_positions.append((x, y))
            self.write_positions()
        elif event == cv2.EVENT_MBUTTONDOWN:
            for index, pos in enumerate(self.car_park_positions):
                x1, y1 = pos
                if x1 <= x <= x1 + self.rect_width and y1 <= y <= y1 + self.rect_height:
                    self.car_park_positions.pop(index)
                    self.write_positions()

    def write_positions(self):
        """Writes car park positions to a pickle file."""
        try:
            with open(self.car_park_positions_path, 'wb') as f:
                pickle.dump(self.car_park_positions, f)
        except Exception as e:
            print(f"Error: {e}\nFailed to write car park positions file.")
