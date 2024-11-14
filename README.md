# motion-based-surveillance-system
This project implements an advanced motion-based surveillance system designed to detect movement, alert the user, and record video clips during activity. Utilizing OpenCV for motion analysis and NumPy for data processing, the system operates by detecting differences between consecutive video frames captured from a live camera feed. Upon detecting movement, it performs the following actions:

Motion Alert: A distinct alert sound (buzzer) is triggered to immediately notify the user of the detected activity.

Video Recording and Display: The system begins recording a high-resolution video of the scene, annotating detected motion with bounding rectangles and displaying real-time activity.

Dynamic Recording Extension: If motion continues beyond a predefined period, the system dynamically extends the recording until the motion ceases.

Snapshot Capture : During motion, snapshots are captured at set intervals, enabling remote monitoring in real-time.

Time-Stamped Log: Each motion event is logged in a text file with a timestamp, duration, and other details, allowing for detailed post-event review.

This system is suitable for applications such as home security or facility monitoring. Below is the modified code to achieve these improvements.
