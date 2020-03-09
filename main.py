from collections import OrderedDict
import json

from routine import Routine

if __name__ == '__main__':
    '''
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
    '''

    # Iterate over different start times to determine the best start time to use
    # third prelim optional actual airtime: ~17.60
    third_prelim_optional = Routine(
        "C://Users//Jeremy//Downloads//third_prelim_optional.wav", 0, 38,
        show_plot=False
    )
    airtimes = OrderedDict()
    initial_start_time = 15
    for time_index in range(75):
        start_time = initial_start_time + time_index * 0.05
        print(f"Calculating airtime for start time of: {start_time}")
        third_prelim_optional.change_start(start_time)
        try:
            airtime = third_prelim_optional.get_airtime()
        except Exception as e:
            print(f"Error: {e}")
            break
        airtimes[start_time] = airtime

    print(f"airtimes: {json.dumps(airtimes, indent=4)}")
