import cv2
import numpy as np
from pyzbar.pyzbar import decode

def scan_barcode():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Decode barcodes in the frame
        barcodes = decode(frame)

        # Loop through detected barcodes
        for barcode in barcodes:
            # Extract barcode data
            barcode_data = barcode.data.decode('utf-8')
            
            # Draw a rectangle around the barcode
            rect_points = barcode.polygon
            if len(rect_points) == 4:
                pts = [(int(rect_points[i].x), int(rect_points[i].y)) for i in range(4)]
                pts = np.array(pts, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.drawContours(frame, [pts], -1, (0, 255, 0), 2)

            # Display barcode data
            cv2.putText(frame, f"Barcode: {barcode_data}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Print barcode data to console
            print("Scanned Barcode:", barcode_data)

        # Display the frame
        cv2.imshow('Barcode Scanner', frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_barcode()
