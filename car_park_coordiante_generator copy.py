import cv2
from src.utils import Coordinate_denoter


def demonstration():
    """Demonstration of the car park coordinate generator."""

    # Creating the Coordinate_denoter instance for extracting car park coordinates
    coordinate_generator = Coordinate_denoter()

    # Read and initialize the coordinates
    coordinate_generator.read_positions()

    # Set initial variables
    image_path = "data/source/example_image.png"
    rect_width, rect_height = coordinate_generator.rect_width, coordinate_generator.rect_height

    # Serve the GUI window until user terminates it
    while True:
        # Refresh the image
        image = cv2.imread(image_path)

        # Draw the current car park coordinates
        for pos in coordinate_generator.car_park_positions:
            # Define boundaries
            start = pos
            end = (pos[0] + rect_width, pos[1] + rect_height)

            # Draw the rectangle on the image (use green color for empty spaces)
            if coordinate_generator.is_space_empty(pos):
                cv2.rectangle(image, start, end, (0, 255, 0), 2)  # Green for empty
            else:
                cv2.rectangle(image, start, end, (0, 0, 255), 2)  # Red for occupied

        cv2.imshow("Image", image)

        # Link the mouse callback
        cv2.setMouseCallback("Image", coordinate_generator.mouseClick)

        # Exit condition
        if cv2.waitKey(1) == ord("q"):
            break

    # Release resources
    cv2.destroyAllWindows()


if __name__ == "__main__":
    demonstration()
