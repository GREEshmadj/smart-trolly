import cv2
import numpy as np
from pyzbar.pyzbar import decode
import openpyxl
import tkinter as tk

class BarcodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode Scanner App")

        # Create an Excel workbook and add a worksheet
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        # List to store scanned barcode data
        self.scanned_data = []

        # Open the webcam
        self.cap = cv2.VideoCapture(0)

        # Create a label to display barcode information
        self.label = tk.Label(root, text="Scanned Barcode: ")
        self.label.pack(pady=10)

        # Create a start button to begin scanning
        self.start_button = tk.Button(root, text="Start Scanning", command=self.scan_barcode)
        self.start_button.pack(pady=10)

        # Create a stop button to stop scanning
        self.stop_button = tk.Button(root, text="Stop Scanning", command=self.stop_scan)
        self.stop_button.pack(pady=10)

    def scan_barcode(self):
        try:
            while True:
                # Read a frame from the webcam
                ret, frame = self.cap.read()

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
                    self.label.config(text=f"Scanned Barcode: {barcode_data}")

                    # Print barcode data to console
                    print("Scanned Barcode:", barcode_data)

                    # Store scanned data in the list
                    self.scanned_data.append(barcode_data)

                # Display the frame
                cv2.imshow('Barcode Scanner', frame)
                self.root.update_idletasks()
                self.root.update()

                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            print("Script terminated by user.")

    def stop_scan(self):
        # Save all scanned data to Excel
        for data in self.scanned_data:
            self.ws.append([data])

        # Save the Excel file
        self.wb.save('all_scanned_data.xlsx')

        # Release the webcam and close all windows
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeScannerApp(root)
    root.mainloop()
