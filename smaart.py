import cv2
from pyzbar.pyzbar import decode

class SmartTrolley:
    def __init__(self):
        self.shopping_list = {}
        self.total_cost = 0

    def scan_item(self, item_name, price):
        if item_name not in self.shopping_list:
            self.shopping_list[item_name] = 1
        else:
            self.shopping_list[item_name] += 1
        self.total_cost += price
        print(f"{item_name} scanned. Current total cost: ${self.total_cost}")

    def display_cart(self):
        print("Shopping Cart:")
        for item, quantity in self.shopping_list.items():
            print(f"{item}: {quantity}")
        print(f"Total Cost: ${self.total_cost}")

    def checkout(self):
        print("Checkout completed. Thank you!")
        self.display_cart()
        self.reset_trolley()

    def reset_trolley(self):
        self.shopping_list = {}
        self.total_cost = 0

    def scan_barcode_from_camera(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            # Convert the frame to grayscale for barcode decoding
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Decode barcodes
            barcodes = decode(gray)

            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                self.scan_item(barcode_data, 10)  # Assuming a constant price for scanned items

            # Display the frame
            cv2.imshow('Barcode Scanner', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

# Example Usage
if __name__ == "__main__":
    trolley = SmartTrolley()
    trolley.scan_barcode_from_camera()
