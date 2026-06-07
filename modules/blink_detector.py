import numpy as np


class BlinkDetector:

    def __init__(self):

        self.EAR_THRESHOLD = 0.22
        self.CONSEC_FRAMES = 2

        self.blink_count = 0
        self.closed_frames = 0

    def distance(self, p1, p2):
        return np.linalg.norm(
            np.array(p1) - np.array(p2)
        )

    def calculate_ear(self, eye_points):

        A = self.distance(
            eye_points[1],
            eye_points[5]
        )

        B = self.distance(
            eye_points[2],
            eye_points[4]
        )

        C = self.distance(
            eye_points[0],
            eye_points[3]
        )

        if C == 0:
            return 0

        ear = (A + B) / (2.0 * C)

        return ear

    def update(self, left_eye, right_eye):

        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)

        ear = (left_ear + right_ear) / 2

        if ear < self.EAR_THRESHOLD:

            self.closed_frames += 1

        else:

            if self.closed_frames >= self.CONSEC_FRAMES:
                self.blink_count += 1

            self.closed_frames = 0

        return ear, self.blink_count

    def get_blink_frequency(self, elapsed_minutes):

        if elapsed_minutes <= 0:
            return 0

        return round(
            self.blink_count / elapsed_minutes,
            2
        )