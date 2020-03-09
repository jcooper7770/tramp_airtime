"""
 Get the airtime of a routine given the audio using the relative peaks of
 the amplitudes of the sound as indications of bounces

 For converting MOV files to WAV: https://convertio.co/
 Getting the relative peaks: https://stackoverflow.com/questions/31070563/find-all-local-maxima-and-minima-when-x-and-y-values-are-given-as-numpy-arrays/31073798

 TODO:
   - Finetune to get the actual airtimes
   - Use ffmpeg or other software to extract audio instead of doing manually
"""

import scipy.io.wavfile
from scipy.signal import argrelextrema, find_peaks
import matplotlib.pyplot as plt
from numpy import greater, asarray
import numpy

def convert_index_to_time(index, video_length, size):
    """
    Converts the given index to a time in the video
    """
    return (index / size) * video_length


class Routine:
    def __init__(self, video_file, start_time, end_time):
        """
        :param video_file: The wav file path
        :type video_file: str
        :param start_time: The start time of the routine in the video (in seconds)
        :type start_time: int
        :param end_time: The end time of the routine in the video (in seconds)
        :type end_time: int
        """
        self.video_file = video_file
        self.start_time = start_time
        self.end_time = end_time

        self.peaks = None
        self.routineJumpsArray = None
        self.routineLength = None

    def get_airtime(self):
        """
        Returns the airtime from the routine

        :return: The airtime of the routine
        :rtype: float
        """
        if self.peaks is None:
            peaks, routineJumpsArray, routineLength = get_peak_sounds(
                self.start_time, self.end_time, self.video_file
            )
            self.peaks = peaks
            self.routineJumpsArray = routineJumpsArray
            self.routineLength = routineLength

        numIndices = len(self.routineJumpsArray)
        timeIndices = [index/numIndices * routineLength for index in range(numIndices)]
        peakTimes = [peak/numIndices * routineLength for peak in self.peaks]
        print(f"Peak times: {peakTimes}")
        #ynormPeaks = [ynormArray[peak] for peak in peaks]
        ynormPeaks = [routineJumpsArray[peak] for peak in self.peaks]
        numPeaks = len(self.peaks)

        # Get the difference between the first peak and the second to last peak
        airtime = peakTimes[-2] - peakTimes[0]
        print(f"airtime: {airtime:.4f}s")

        # Plot the normalized values
        #plt.plot(timeIndices, ynormArray)
        plt.plot(timeIndices, self.routineJumpsArray)

        # Plot the  values above 0.2 and below 0.3
        #plt.plot(timeIndices, maxValues)

        # Plot the peaks
        #plt.plot(peakTimes, ynormArray[peaks], "x")
        plt.plot(peakTimes, self.routineJumpsArray[peaks], "x")
        plt.show()

        return airtime

    def create_jump_wav(self, wav_file):
        """
        Creates a wav file with only jumps

        :param wav_file: The file to save to
        :type wav_file: str
        """
        # Get the peaks
        if self.peaks is None:
            peaks, routineJumpsArray, routineLength = get_peak_sounds(
                self.start_time, self.end_time, self.video_file
            )
            self.peaks = peaks
            self.routineJumpsArray = routineJumpsArray
            self.routineLength = routineLength


        # Create an array with only the times surrounding the peaks
        cushion = 15000
        jumps = []

        length = len(self.routineJumpsArray)
        for index in range(length):
            is_inside_peak = False
            for peakIndex in self.peaks:
                if index - cushion < peakIndex < index + cushion:
                    is_inside_peak = True
                    break

            if is_inside_peak:
                jumps.append([self.routineJumpsArray[index], self.routineJumpsArray[index]])
            else:
                jumps.append([0,0])

        jumpsArray =  asarray(jumps, dtype=numpy.int16)
        scipy.io.wavfile.write(wav_file, 44100, jumpsArray)


def get_peak_sounds(start_time, end_time, video_file):
    """
    Returns the peak information

    :param start_time: The start time of the routine in the video (in seconds)
    :type start_time: int
    :param end_time: The end time of the routine in the video (in seconds)
    :type end_time: int
    :param video_file: The wav file path
    :type video_file: str

    :return: The peak indices, the routine array, and the routine length
    :rtype: Tuple<np.array, np.array, int>
    """
    x = scipy.io.wavfile.read(video_file)
    #print(x)
    y = x[1]
    totalNumIndices = len(y)
    #times = numpy.linspace(0., y.shape[0]/x[0], y.shape[0])
    #print(times)

    routineStartTime = start_time
    
    #videoLength = video_length
    videoLength = y.shape[0]/x[0]
    routineEndTime = end_time if end_time > 0 else videoLength
    print(f"Video length: {videoLength:.2f}s")
    routineLength = routineEndTime - routineStartTime
    startIndex = int(totalNumIndices * (routineStartTime / videoLength))
    endIndex = int(totalNumIndices * (routineEndTime / videoLength))

    routineJumps = [y[i] for i in range(startIndex, endIndex)]

    # Add times to x axis
    numIndices = len(routineJumps)
    
    # Get relative extrema
    routineJumpsArray = asarray(routineJumps)
    extrema = argrelextrema(routineJumpsArray, greater)
    numExtrema = len(extrema[0])

    # Find the peaks
    # fix the array
    if type(routineJumpsArray[0]) == numpy.ndarray:
        routineJumpsArray = asarray([numpy.average(value) for value in routineJumps])
    
    peaks, _ = find_peaks(routineJumpsArray, distance=len(routineJumpsArray)/18)
    #peaks, _ = find_peaks(ynormArray, height=0.2, distance=len(ynorm)/18)
    return peaks, routineJumpsArray, routineLength


print("Third prelim optional")
third_prelim_optional = Routine("C://Users//Jeremy//Downloads//third_prelim_optional.wav", 19, 38)
third_prelim_optional.get_airtime()

print("\nThird prelim compulsory")
third_prelim_comp = Routine("C://Users//Jeremy//Downloads//third_prelim_comp.wav", 15, 34)

third_prelim_comp.get_airtime()

print("\nCompulsory at the gym")
gym_comp = Routine("C://Users//Jeremy//Downloads//compulsory.wav", 1, 21)
gym_comp.get_airtime()
gym_comp.create_jump_wav("jumps.wav")

print("\nVIP Classic compulsory")
vip_comp = Routine("C://Users//Jeremy//Downloads//vip_comp.wav", 0, 19)
vip_comp.get_airtime()

