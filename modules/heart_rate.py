class HeartRateEstimator:

    def __init__(self):

        # Wider valid BPM range
        self.min_bpm = 40
        self.max_bpm = 180

        # Store recent BPM values for smoothing
        self.bpm_history = []
        self.max_history = 5

    def calculate_bpm(self, frequency):

        if frequency is None:
            return None

        bpm = frequency * 60

        if bpm < self.min_bpm:
            return None

        if bpm > self.max_bpm:
            return None

        return round(bpm)

    def smooth_bpm(self, bpm):

        if bpm is None:
            return None

        self.bpm_history.append(bpm)

        if len(self.bpm_history) > self.max_history:
            self.bpm_history.pop(0)

        return round(
            sum(self.bpm_history) /
            len(self.bpm_history)
        )

    def reset(self):

        self.bpm_history.clear()

    def get_display_values(self, frequency):

        if frequency is None:
            return "N/A", "N/A"

        bpm = self.calculate_bpm(
            frequency
        )

        if bpm is None:
            return "N/A", "N/A"

        bpm = self.smooth_bpm(
            bpm
        )

        return (
            f"{frequency:.2f} Hz",
            f"{bpm} BPM"
        )