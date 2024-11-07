import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

distance_left = ctrl.Antecedent(np.arange(0, 201, 1), 'distance_left')
distance_right = ctrl.Antecedent(np.arange(0, 201, 1), 'distance_right')
distance_back = ctrl.Antecedent(np.arange(0, 201, 1), 'distance_back')
parking_status = ctrl.Consequent(np.arange(0, 101, 1), 'parking_status')

# distance_left

distance_left['crash'] = fuzz.trimf(distance_left.universe, [0, 0, 5])
distance_left['close'] = fuzz.trimf(distance_left.universe, [5, 20, 50])
distance_left['medium'] = fuzz.trimf(distance_left.universe, [20, 50, 100])
distance_left['far'] = fuzz.trimf(distance_left.universe, [50, 100, 200])


# distance_right

distance_right['crash'] = fuzz.trimf(distance_left.universe, [0, 0, 5])
distance_right['close'] = fuzz.trimf(distance_right.universe, [5, 20, 50])
distance_right['medium'] = fuzz.trimf(distance_right.universe, [20, 50, 100])
distance_right['far'] = fuzz.trimf(distance_right.universe, [50, 100, 200])


# distance_back

distance_back['crash'] = fuzz.trimf(distance_left.universe, [0, 0, 5])
distance_back['close'] = fuzz.trimf(distance_back.universe, [5, 20, 50])
distance_back['medium'] = fuzz.trimf(distance_back.universe, [20, 50, 100])
distance_back['far'] = fuzz.trimf(distance_back.universe, [50, 100, 200])


# parking_status
parking_status['crashh'] = fuzz.trimf(parking_status.universe, [0, 0, 10])
parking_status['bad'] = fuzz.trimf(parking_status.universe, [5, 20, 50])
parking_status['average'] = fuzz.trimf(parking_status.universe, [30, 60, 90])
parking_status['perfect'] = fuzz.trimf(parking_status.universe, [70, 100, 100])


rule_bad = ctrl.Rule(
    (distance_left['close'] | distance_right['close'] | distance_back['close']),
    consequent=parking_status['bad']
)

rule_perfect = ctrl.Rule(
    (distance_left['medium'] & distance_right['medium'] & distance_back['medium']),
    consequent=parking_status['perfect']
)

rule_average = ctrl.Rule(
    (distance_left['far'] & distance_right['far'] & distance_back['far']) |
    (distance_left['medium'] & distance_right['far'] & distance_back['medium']) |
    (distance_left['medium'] & distance_right['medium'] & distance_back['far']) |
    (distance_left['far'] & distance_right['far'] & distance_back['medium']) |
    (distance_left['far'] & distance_right['medium'] & distance_back['far']) |
    (distance_left['far'] & distance_right['medium'] & distance_back['medium']),
    consequent=parking_status['average']
)

rule_crash = ctrl.Rule(
    antecedent=(
        (distance_left['crash']) | (distance_right['crash']) | (distance_back['crash'])
    ),
    consequent=parking_status['crashh']
)

parking_status_ctrl = ctrl.ControlSystem([rule_crash, rule_bad, rule_average, rule_perfect])
parking_status_sim = ctrl.ControlSystemSimulation(parking_status_ctrl)

left = int(input("Provide left distance: "))
right = int(input("Provide right distance: "))
back = int(input("Provide baqck distance: "))

parking_status_sim.input['distance_left'] = left
parking_status_sim.input['distance_right'] = right
parking_status_sim.input['distance_back'] = back

parking_status_sim.compute()
parking_status.view(sim=parking_status_sim)
print(round(parking_status_sim.output['parking_status'], 1))
plt.show()

# distance_left.view()
# distance_right.view()
# distance_back.view()
# plt.show()
