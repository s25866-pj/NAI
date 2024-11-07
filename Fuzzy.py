"""
Daria Szabłowska - s24967
Damian Grzesiak - s25866

URUCHOMIENIE:
Aby zainstalować potrzebne biblioteki należy wpisać komendę:
pip install -r requirements.txt

O PROJEKCIE:
Jest to projekt służący do oceny parkowania auta, na podstawie wykrytych przez czujniki odległości od przeszkód.

"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
class ParkingSystem:
    def __init__(self):
        self.distance_left = ctrl.Antecedent(np.arange(0, 201, 1), 'distance_left')
        self.distance_right = ctrl.Antecedent(np.arange(0, 201, 1), 'distance_right')
        self.distance_back = ctrl.Antecedent(np.arange(0, 201, 1), 'distance_back')
        self.parking_status = ctrl.Consequent(np.arange(0, 101, 1), 'parking_status')

        self._define_membership_functions()

        self.parking_status_ctrl = ctrl.ControlSystem([self.rule_crash(), self.rule_bad(), self.rule_average(), self.rule_perfect()])
        self.parking_status_sim = ctrl.ControlSystemSimulation(self.parking_status_ctrl)

    def _define_membership_functions(self):

        # distance_left

        self.distance_left['crash'] = fuzz.trimf(self.distance_left.universe, [0, 0, 5])
        self.distance_left['close'] = fuzz.trimf(self.distance_left.universe, [5, 20, 50])
        self.distance_left['medium'] = fuzz.trimf(self.distance_left.universe, [20, 50, 100])
        self.distance_left['far'] = fuzz.trimf(self.distance_left.universe, [50, 100, 200])


        # distance_right

        self.distance_right['crash'] = fuzz.trimf(self.distance_left.universe, [0, 0, 5])
        self.distance_right['close'] = fuzz.trimf(self.distance_right.universe, [5, 20, 50])
        self.distance_right['medium'] = fuzz.trimf(self.distance_right.universe, [20, 50, 100])
        self.distance_right['far'] = fuzz.trimf(self.distance_right.universe, [50, 100, 200])


        # distance_back

        self.distance_back['crash'] = fuzz.trimf(self.distance_left.universe, [0, 0, 5])
        self.distance_back['close'] = fuzz.trimf(self.distance_back.universe, [5, 20, 50])
        self.distance_back['medium'] = fuzz.trimf(self.distance_back.universe, [20, 50, 100])
        self.distance_back['far'] = fuzz.trimf(self.distance_back.universe, [50, 100, 200])


        # parking_status
        self.parking_status['crashh'] = fuzz.trimf(self.parking_status.universe, [0, 0, 10])
        self.parking_status['bad'] = fuzz.trimf(self.parking_status.universe, [5, 20, 50])
        self.parking_status['average'] = fuzz.trimf(self.parking_status.universe, [30, 60, 90])
        self.parking_status['perfect'] = fuzz.trimf(self.parking_status.universe, [70, 100, 100])


    def rule_bad(self):
        return ctrl.Rule(
            (self.distance_left['close'] | self.distance_right['close'] | self.distance_back['close']),
            consequent=self.parking_status['bad']
        )

    def rule_perfect(self): 
        return ctrl.Rule(
            (self.distance_left['medium'] & self.distance_right['medium'] & self.distance_back['medium']),
            consequent=self.parking_status['perfect']
        )

    def rule_average(self): 
        return ctrl.Rule(
            (self.distance_left['far'] & self.distance_right['far'] & self.distance_back['far']) |
            (self.distance_left['medium'] & self.distance_right['far'] & self.distance_back['medium']) |
            (self.distance_left['medium'] & self.distance_right['medium'] & self.distance_back['far']) |
            (self.distance_left['far'] & self.distance_right['far'] & self.distance_back['medium']) |
            (self.distance_left['far'] & self.distance_right['medium'] & self.distance_back['far']) |
            (self.distance_left['far'] & self.distance_right['medium'] & self.distance_back['medium']),
            consequent=self.parking_status['average']
        )

    def rule_crash(self): 
        return ctrl.Rule(
            antecedent=(
                (self.distance_left['crash']) | (self.distance_right['crash']) | (self.distance_back['crash'])
            ),
            consequent=self.parking_status['crashh']
        )

    def get_parking_status(self, left, right, back):

        self.parking_status_sim.input['distance_left'] = left
        self.parking_status_sim.input['distance_right'] = right
        self.parking_status_sim.input['distance_back'] = back

        self.parking_status_sim.compute()

        return round(self.parking_status_sim.output['parking_status'], 1)

    def show_parking_status_plot(self):
        
        self.parking_status.view(sim=self.parking_status_sim)
        plt.show()

def main():

    parking_system = ParkingSystem()

    left = int(input("Provide left distance: "))
    right = int(input("Provide right distance: "))
    back = int(input("Provide back distance: "))

    status = parking_system.get_parking_status(left, right, back)
    print(f"Parking status: {status}")

    parking_system.show_parking_status_plot()


if __name__ == "__main__":
    main()




