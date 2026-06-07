import cv2
from mediapipe.python.solutions import face_mesh


class EyeDetector:

    def __init__(self):

        self.face_mesh = face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.left_eye_ids = [33, 160, 158, 133, 153, 144]
        self.right_eye_ids = [362, 385, 387, 263, 373, 380]

    def detect_eyes(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return False, None, None

        landmarks = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        left_eye = []
        right_eye = []

        # Left eye points
        for idx in self.left_eye_ids:

            lm = landmarks.landmark[idx]

            x = int(lm.x * w)
            y = int(lm.y * h)

            left_eye.append((x, y))

        # Right eye points
        for idx in self.right_eye_ids:

            lm = landmarks.landmark[idx]

            x = int(lm.x * w)
            y = int(lm.y * h)

            right_eye.append((x, y))

        # Validate both eyes exist
        if len(left_eye) != 6:
            return False, None, None

        if len(right_eye) != 6:
            return False, None, None

        # Validate coordinates are inside frame
        for x, y in left_eye + right_eye:

            if x <= 0 or y <= 0:
                return False, None, None

            if x >= w or y >= h:
                return False, None, None

        return True, left_eye, right_eye