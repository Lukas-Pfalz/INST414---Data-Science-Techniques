
# Organization:
# Columns = Tricep "Exercises"
# Exercises:
name = {"Tricep Kickbacks", "Overhead Tricep Extension", "Bar Pushdowns", "Closed Grip Bench Press", "Lying Barbell Triceps Extension", "Bench Dips"}

# Muscle Activation in Tricep Heads (Overall)
# (Data from: https://www.acefitness.org/certifiednewsarticle/3008/ace-study-identifies-best-triceps-exercises/?srsltid=AfmBOoqTH6OITUFgH9tLCFIUjQcskTO71JZ6CMwjo0fyDNoGgKxNj1Mp)
# triceps kickbacks (100.29)
# overhead triceps extensions (84.045)
# bar push-downs (77.24)
# rope push-downs (85.32)
# closed-grip bench press (15.88)
# lying barbell triceps extensions (70.125)
# dips (96.935)
emg = [100.29, 84.045, 77.24, 85.32, 15.88, 70.125, 96.935]

# ROM = % Change in "Angle Motion Range for Exercises"
# (Data from: https://www.researchgate.net/publication/389632452_Partial_versus_full_range_of_motion_triceps_strength_training_on_shooting_accuracy_among_recreational_basketball_players_a_randomized_controlled_trial?utm_source=chatgpt.com)
# triceps kickbacks (45%)
# overhead triceps extensions (93%)
# bar push-downs (65%)
# rope push-downs (72%)
# closed-grip bench press (62%)
# lying barbell triceps extensions (87%)
# dips (69%)
rom = [0.45, 0.93, 0.65, 0.72, 0.62, 0.87, 0.69]

# Loading Potential = How Heavily exercise can be loaded
# (Data from: https://strengthlevel.com/strength-standards/tricep-extension/lb?utm_source=chatgpt.com)
# triceps kickbacks (0.30)
# overhead triceps extensions (0.925)
# bar push-downs (0.475)
# rope push-downs (0.55)
# closed-grip bench press (0.75)
# lying barbell triceps extensions (0.85)
# dips (0.625)
load = [0.30, 0.925, 0.475, 0.55, 0.75, 0.85, 0.625]

# Mean is
# Variance accounts for any skewed outlier, since averages only measure an average through the
# group, but considering the 'DISTRIBUTION' of the normal person

# Create Dictionary to store pairs of
# - "Tricep Exercise Name" = String
# - "Array of 'Effectiveness'per Head" = {Eff_LngH (Double), Eff_LtrH (Double), Eff_MH (Double)}
effectiveness = []

# Loop through the Tricep-Exercise-Factor Values measured
temp_emg = 0
temp_rom = 0
temp_load = 0
temp_effectiveness = 0
for i in range(len(name)):
    temp_emg = emg[i]
    temp_rom = rom[i]
    temp_load = load[i]
    temp_effectiveness = temp_emg * temp_rom * temp_load
    effectiveness.append(temp_effectiveness)

# So long as the validated research can
# You can't multiply it together just to do-it, but you can create a composite score
# When considering exercise, you need to consider it for specific TYPE of effectiveness
#

# Store the Set in the Dictionary pairing "Exercise Name" and "Effectiveness Array"
scores = dict(zip(name, effectiveness))
print(scores)

# sorted_items = sorted(scores.items(), key=lambda item: item[1], reverse=True)
# print(sorted_items)
# Sort the "Effectiveness" for Each Muscle Head (Most to Least)
# for key, value in scores.items():
    # print(f"{key} - Effectiveness Score: {value}")
