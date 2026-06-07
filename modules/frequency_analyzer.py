import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
from scipy.fft import fft, fftfreq


class FrequencyAnalyzer:

    def __init__(self):

        # Human heart rate range
        # 0.75 Hz = 45 BPM
        # 3.0 Hz = 180 BPM
        self.lowcut = 0.75
        self.highcut = 3.0

        self.filter_order = 3

    def bandpass_filter(self, signal, fs):

        nyquist = fs * 0.5

        if nyquist <= self.highcut:
            return signal

        low = self.lowcut / nyquist
        high = self.highcut / nyquist

        b, a = butter(
            self.filter_order,
            [low, high],
            btype="band"
        )

        filtered = filtfilt(
            b,
            a,
            signal
        )

        return filtered

    def validate_signal(self, signal):

        if len(signal) < 60:
            return False

        if np.std(signal) < 0.5:
            return False

        return True

    def validate_peaks(self, filtered_signal):

        peaks, _ = find_peaks(
            filtered_signal,
            distance=3
        )

        return len(peaks) >= 2

    def analyze(self, signal_buffer, time_buffer):

        try:

            if len(signal_buffer) < 60:
                return None

            duration = (
                time_buffer[-1] -
                time_buffer[0]
            )

            if duration <= 0:
                return None

            fs = len(signal_buffer) / duration

            if fs < 2:
                return None

            signal = np.array(
                signal_buffer,
                dtype=np.float64
            )

            if not self.validate_signal(signal):
                return None

            # Remove DC component
            signal = signal - np.mean(signal)

            # Normalize
            std = np.std(signal)

            if std > 0:
                signal = signal / std

            filtered = self.bandpass_filter(
                signal,
                fs
            )

            if len(filtered) < 20:
                return None

            if not self.validate_peaks(filtered):
                return None

            n = len(filtered)

            yf = np.abs(
                fft(filtered)
            )

            xf = fftfreq(
                n,
                1 / fs
            )

            positive = xf > 0

            xf = xf[positive]
            yf = yf[positive]

            valid = (
                (xf >= self.lowcut) &
                (xf <= self.highcut)
            )

            xf = xf[valid]
            yf = yf[valid]

            if len(xf) == 0:
                return None

            if len(yf) == 0:
                return None

            dominant_index = np.argmax(yf)

            dominant_frequency = float(
                xf[dominant_index]
            )

            if dominant_frequency < self.lowcut:
                return None

            if dominant_frequency > self.highcut:
                return None

            return round(
                dominant_frequency,
                2
            )

        except Exception as e:

            print(
                "Frequency Analyzer Error:",
                e
            )

            return None