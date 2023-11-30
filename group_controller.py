from kesslergame import KesslerController
from skfuzzy import fuzz
from skfuzzy import control as ctrl
import math
import numpy as np


class group_controller(KesslerController):

    def __init__(self):
        self.eval_frames = 0

        # Input: Current ship velocity (-240.0, 240.0) m/s^2
        ship_current_speed = ctrl.Antecedent(np.arange(-240, 240, 1), 'ship_current_speed')
        ship_current_speed['negative_fast'] = fuzz.trimf(ship_current_speed.universe, [-240, -240, -120])
        ship_current_speed['negative_slow'] = fuzz.trimf(ship_current_speed.universe, [-240, -120, 0])
        ship_current_speed['zero'] = fuzz.trimf(ship_current_speed.universe, [-60, 0, 60])
        ship_current_speed['positive_slow'] = fuzz.trimf(ship_current_speed.universe, [0, 120, 240])
        ship_current_speed['positive_fast'] = fuzz.trimf(ship_current_speed.universe, [120, 240, 240])

        # Input: Current enemy ship velocity (-240.0, 240.0) m/s^2
        enemy_current_speed = ctrl.Antecedent(np.arange(-240, 240, 1), 'enemy_current_speed')
        enemy_current_speed['negative_fast'] = fuzz.trimf(enemy_current_speed.universe, [-240, -240, -120])
        enemy_current_speed['negative_slow'] = fuzz.trimf(enemy_current_speed.universe, [-240, -120, 0])
        enemy_current_speed['zero'] = fuzz.trimf(enemy_current_speed.universe, [-60, 0, 60])
        enemy_current_speed['positive_slow'] = fuzz.trimf(enemy_current_speed.universe, [0, 120, 240])
        enemy_current_speed['positive_fast'] = fuzz.trimf(enemy_current_speed.universe, [120, 240, 240])

        # Input: Current ship distance from ship to asteroid (0.0, 1000.0) m
        current_distance = ctrl.Antecedent(np.arange(0, 1000, 1), 'current_distance')
        current_distance['super_close'] = fuzz.trimf(current_distance.universe, [0, 0, 100])
        current_distance['close'] = fuzz.trimf(current_distance.universe, [0, 100, 200])
        current_distance['medium'] = fuzz.trimf(current_distance.universe, [100, 200, 300])
        current_distance['far'] = fuzz.trimf(current_distance.universe, [200, 300, 400])
        current_distance['super_far'] = fuzz.trimf(current_distance.universe, [300, 400, 1000])

        # Input: Current ship angle from ship to asteroid (-pi, pi) rad
        ship_asteroid_angle = ctrl.Antecedent(np.arange(-math.pi, math.pi, 0.01), 'ship_asteroid_angle')
        ship_asteroid_angle['negative_large'] = fuzz.zmf(ship_asteroid_angle.universe, -1*math.pi/3,-1*math.pi/6)
        ship_asteroid_angle['negative_small'] = fuzz.trimf(ship_asteroid_angle.universe, [-1*math.pi/3,-1*math.pi/6,0])
        ship_asteroid_angle['zero'] = fuzz.trimf(ship_asteroid_angle.universe, [-1*math.pi/6,0,math.pi/6])
        ship_asteroid_angle['positive_small'] = fuzz.trimf(ship_asteroid_angle.universe, [0,math.pi/6,math.pi/3])
        ship_asteroid_angle['positive_large'] = fuzz.smf(ship_asteroid_angle.universe,math.pi/6,math.pi/3)

        # Input: Current asteroid moving angle (-pi, pi) rad
        asteroid_moving_angle = ctrl.Antecedent(np.arange(-math.pi, math.pi, 0.01), 'asteroid_moving_angle')
        asteroid_moving_angle['negative_large'] = fuzz.zmf(asteroid_moving_angle.universe, -1*math.pi/3,-1*math.pi/6)
        asteroid_moving_angle['negative_small'] = fuzz.trimf(asteroid_moving_angle.universe, [-1*math.pi/3,-1*math.pi/6,0])
        asteroid_moving_angle['zero'] = fuzz.trimf(asteroid_moving_angle.universe, [-1*math.pi/6,0,math.pi/6])
        asteroid_moving_angle['positive_small'] = fuzz.trimf(asteroid_moving_angle.universe, [0,math.pi/6,math.pi/3])
        asteroid_moving_angle['positive_large'] = fuzz.smf(asteroid_moving_angle.universe,math.pi/6,math.pi/3)

        # Input: Current ship angle from ship to enemy ship (-pi, pi) rad
        ship_enemy_angle = ctrl.Antecedent(np.arange(-math.pi, math.pi, 0.01), 'ship_enemy_angle')
        ship_enemy_angle['negative_large'] = fuzz.zmf(ship_enemy_angle.universe, -1*math.pi/3,-1*math.pi/6)
        ship_enemy_angle['negative_small'] = fuzz.trimf(ship_enemy_angle.universe, [-1*math.pi/3,-1*math.pi/6,0])
        ship_enemy_angle['zero'] = fuzz.trimf(ship_enemy_angle.universe, [-1*math.pi/6,0,math.pi/6])
        ship_enemy_angle['positive_small'] = fuzz.trimf(ship_enemy_angle.universe, [0,math.pi/6,math.pi/3])
        ship_enemy_angle['positive_large'] = fuzz.smf(ship_enemy_angle.universe,math.pi/6,math.pi/3)

        # Input: Asteroid size small, medium, large, huge
        asteroid_size = ctrl.Antecedent(np.arange(0, 100, 1), 'asteroid_size')
        asteroid_size['small'] = fuzz.trimf(asteroid_size.universe, [0, 0, 25])
        asteroid_size['medium'] = fuzz.trimf(asteroid_size.universe, [0, 25, 50])
        asteroid_size['large'] = fuzz.trimf(asteroid_size.universe, [25, 50, 75])
        asteroid_size['huge'] = fuzz.trimf(asteroid_size.universe, [50, 75, 100])

        # Input: ship health
        ship_health = ctrl.Antecedent(np.arange(1, 4, 1), 'ship_health')
        ship_health['three_hits_left'] = fuzz.trimf(ship_health.universe, [3, 3, 3])
        ship_health['two_hits_left'] = fuzz.trimf(ship_health.universe, [2, 2, 2])
        ship_health['one_hit_left'] = fuzz.trimf(ship_health.universe, [1, 1, 1])

        # Input: Enemy ship health
        enemy_health = ctrl.Antecedent(np.arange(1, 4, 1), 'enemy_health')
        enemy_health['three_hits_left'] = fuzz.trimf(enemy_health.universe, [3, 3, 3])
        enemy_health['two_hits_left'] = fuzz.trimf(enemy_health.universe, [2, 2, 2])
        enemy_health['one_hit_left'] = fuzz.trimf(enemy_health.universe, [1, 1, 1])

        # Output: Ship thrust (-480.0, 480.0) m/s^2
        thrust = ctrl.Consequent(np.arange(-480, 480, 1), 'thrust')
        thrust['negative_fast'] = fuzz.trimf(thrust.universe, [-480, -480, -240])
        thrust['negative_slow'] = fuzz.trimf(thrust.universe, [-480, -240, 0])
        thrust['zero'] = fuzz.trimf(thrust.universe, [-120, 0, 120])
        thrust['positive_slow'] = fuzz.trimf(thrust.universe, [0, 240, 480])
        thrust['positive_fast'] = fuzz.trimf(thrust.universe, [240, 480, 480])

        # Output: Ship rotation 
        ship_rotation = ctrl.Consequent(np.arange(-180,180,1), 'ship_rotation')
        ship_rotation['negative_large'] = fuzz.zmf(ship_rotation.universe, [-180,-180,-30])
        ship_rotation['negative_small'] = fuzz.trimf(ship_rotation.universe, [-180,-30,0])
        ship_rotation['zero'] = fuzz.trimf(ship_rotation.universe, [-30,0,30])
        ship_rotation['positive_small'] = fuzz.trimf(ship_rotation.universe, [0,30,180])
        ship_rotation['positive_large'] = fuzz.smf(ship_rotation.universe, [30,180,180])

        # Output: Fire
        fire = ctrl.Consequent(np.arange(0,2,1), 'fire')
        fire['yes'] = fuzz.trimf(fire.universe, [0,0,1])
        fire['no'] = fuzz.trimf(fire.universe, [0,1,1])








