1. Import necessary libraries: 
   -OpenCV
   -threading
   -playsound
   -email utilities
   -MySQL
   -regex

2. Load the fire detection cascade model:
   - fire_cascade = Load fire detection cascade XML file.

3. Initialize webcam for video capture:
   - vid = Open webcam.

4. Initialize a flag:
   - runOnce = False (Ensures alerts are sent only once).

5. Define a function to fetch employee contacts from the database:
   - Connect to MySQL database.
   - Execute query to fetch email, phone, and carrier details.
   - Close the connection.
   - Return the list of contacts.

6. Define a function to play the fire alarm sound:
   - Use `playsound` to play an alarm audio file.

7. Define a function to send alerts (email and SMS):
   - Fetch contacts from the database.
   - Set up an email server using SMTP.
   - Prepare an alert message (both email and SMS format).
   - Send email notifications to all contacts.
   - Send SMS notifications using carrier-specific gateways.
   - Close the email server connection.

8. Start the main loop for video processing:
   - Read frames from the webcam.
   - Convert frame to grayscale.
   - Detect fire using the cascade model.

9. For each detected fire:
   - Draw a rectangle around the detected fire region.
   - Start a thread to play the alarm sound.
   - If `runOnce` is False:
       - Start a thread to send alerts.
       - Set `runOnce = True`.
   - Else:
       - Print that alerts have already been sent.

10. Display the video feed with fire detection rectangles.

11. Exit the program if the 'q' key is pressed:
    - Release webcam resources.
    - Close all OpenCV windows.
