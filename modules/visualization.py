import cv2


class Visualization:

    def __init__(self):
        pass

    def draw_eye_points(
        self,
        frame,
        left_eye,
        right_eye
    ):

        if left_eye:

            for point in left_eye:

                cv2.circle(
                    frame,
                    point,
                    2,
                    (0, 255, 0),
                    -1
                )

        if right_eye:

            for point in right_eye:

                cv2.circle(
                    frame,
                    point,
                    2,
                    (0, 255, 0),
                    -1
                )

    def draw_roi(
        self,
        frame,
        left_eye,
        right_eye
    ):

        if not left_eye or not right_eye:
            return

        points = left_eye + right_eye

        x_min = min(p[0] for p in points) - 10
        y_min = min(p[1] for p in points) - 10

        x_max = max(p[0] for p in points) + 10
        y_max = max(p[1] for p in points) + 10

        cv2.rectangle(
            frame,
            (x_min, y_min),
            (x_max, y_max),
            (255, 0, 0),
            2
        )

    def draw_dashboard(
        self,
        frame,
        eye_status,
        blink_count,
        blink_freq,
        frequency,
        heart_rate
    ):

        cv2.putText(
            frame,
            f"Eye Status : {eye_status}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Blink Count : {blink_count}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Blink Freq : {blink_freq}/min",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Frequency : {frequency}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Heart Rate : {heart_rate}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

    def show_frame(
        self,
        frame
    ):

        cv2.imshow(
            "Heart Rate Detection Using Retina",
            frame
        )