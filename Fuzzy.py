import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

distance_left = ctrl.Antecedent(np.arange(0, 250, 1), 'distance left')
distance_right = ctrl.Antecedent(np.arange(0, 250, 1), 'distance right')
wheel_turn = ctrl.Consequent(np.arange(-35, 35, 1), 'wheel_turn')
speed = ctrl.Consequent(np.arange(0, 20, 1), 'speed')

# distance_left
distance_left['very_close'] = fuzz.trimf(distance_left.universe, [0, 0, 20])
distance_left['close'] = fuzz.trimf(distance_left.universe, [0, 20, 50])
distance_left['medium'] = fuzz.trimf(distance_left.universe, [20, 50, 100])
distance_left['far'] = fuzz.trimf(distance_left.universe, [50, 100, 200])
distance_left['very_far'] = fuzz.trimf(distance_left.universe, [100, 200, 250])

# distance_right
distance_right['very_close'] = fuzz.trimf(distance_right.universe, [0, 0, 20])
distance_right['close'] = fuzz.trimf(distance_right.universe, [0, 20, 50])
distance_right['medium'] = fuzz.trimf(distance_right.universe, [20, 50, 100])
distance_right['far'] = fuzz.trimf(distance_right.universe, [50, 100, 200])
distance_right['very_far'] = fuzz.trimf(distance_right.universe, [100, 200, 250])

#  wheel_turn 
wheel_turn['strong_left'] = fuzz.trimf(wheel_turn.universe, [-35, -35, -15])
wheel_turn['slight_left'] = fuzz.trimf(wheel_turn.universe, [-20, -10, 0])
wheel_turn['straight'] = fuzz.trimf(wheel_turn.universe, [-5, 0, 5])
wheel_turn['slight_right'] = fuzz.trimf(wheel_turn.universe, [0, 10, 20])
wheel_turn['strong_right'] = fuzz.trimf(wheel_turn.universe, [15, 35, 35])

# speed
speed['stop'] = fuzz.trimf(speed.universe, [0, 0, 5])
speed['slow'] = fuzz.trimf(speed.universe, [0, 5, 10])
speed['fast'] = fuzz.trimf(speed.universe, [10, 20, 20])

distance_left.view()
distance_right.view()
wheel_turn.view()
speed.view()
plt.show()
