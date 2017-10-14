import numpy as np


def initialize_centroids(angles, k):
    """returns k centroids from the initial points"""
    centroids = angles.copy()
    np.random.shuffle(centroids)
    return centroids[:k]

def closest_centroid(angles, centroids):
    """returns an array containing the index to the nearest centroid for each point"""
    distances = []
    for angle in angles:
        dist1 = abs(angle-centroids[0])
        dist2 = abs(angle-centroids[1])
        distances.append([dist1, dist2])
    return np.argmin(distances, axis=1)

def move_centroids(angles, closest, centroids):
    """returns the new centroids assigned from the points closest to them"""
    return np.array([angles[closest==k].mean() for k in range(2)])


def forward_mode(Rover):

    def stuck_check(Rover):
        if Rover.vel < 0.05:
            Rover.stuck_count += 1
        else:
            Rover.stuck_count = 0

        if Rover.stuck_count > 100:
            Rover.mode = 'stuck'
            Rover.stuck_count = 0

    def throttle_control(Rover):
        if Rover.vel < Rover.max_vel:
            # Set throttle value top throttle setting
            Rover.throttle = Rover.throttle_set*(len(Rover.nav_angles)/5000)
        else:  # Else coast
            Rover.throttle = 0
        Rover.brake = 0

    def steer_control(Rover):
        Rover.steer = np.clip((np.mean(Rover.nav_angles) + np.std(Rover.nav_angles)/2)* 180 / np.pi, -20, 20)

        # nav_angle_std = np.std(Rover.nav_angles)
        # if nav_angle_std < 0.4:
        #     print('go straight')
        #     Rover.steer = np.clip(np.mean(Rover.nav_angles) * 180 / np.pi, -10, 10)
        # else:
        #     print('cross road')
        #     centroids = initialize_centroids(Rover.nav_angles, 2)
        #     for _ in range(5):
        #         closest = closest_centroid(Rover.nav_angles, centroids)
        #         centroids = move_centroids(Rover.nav_angles, closest, centroids)
        #         # print(centroids)
        #     sorted(centroids)
        #
        #     Rover.steer = np.clip(centroids[0] * 180 / np.pi, -20, 20)

    # Check the extent of navigable terrain
    if len(Rover.nav_angles) >= Rover.stop_forward:

        print('velocity = ', Rover.vel)
        print('stuck_count =', Rover.stuck_count)
        stuck_check(Rover)
        throttle_control(Rover)
        steer_control(Rover)

    # If there's a lack of navigable terrain pixels then go to 'stop' mode
    elif len(Rover.nav_angles) < Rover.stop_forward:
        # Set mode to "stop" and hit the brakes!
        Rover.throttle = 0
        # Set brake to stored brake value
        Rover.brake = Rover.brake_set
        Rover.steer = 0
        Rover.mode = 'stop'

def stop_mode(Rover):
    print('stop')
    # If we're in stop mode but still moving keep braking
    if Rover.vel > 0.2:
        Rover.throttle = 0
        Rover.brake = Rover.brake_set
        Rover.steer = 0
    # If we're not moving (vel < 0.2) then do something else
    elif Rover.vel <= 0.2:
        # Now we're stopped and we have vision data to see if there's a path forward
        if len(Rover.nav_angles) < Rover.go_forward:
            Rover.throttle = 0
            # Release the brake to allow turning
            Rover.brake = 0
            # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
            Rover.steer = -50  # Could be more clever here about which way to turn
        # If we're stopped but see sufficient navigable terrain in front then go!
        if len(Rover.nav_angles) >= Rover.go_forward:
            # Set throttle back to stored value
            Rover.throttle = Rover.throttle_set
            # Release the brake
            Rover.brake = 0
            # Set steer to mean angle
            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180 / np.pi), -15, 15)
            Rover.mode = 'forward'

def stuck_mode(Rover):
    print('stuck')
    # Set steer to mean angle
    Rover.steer = 10
    Rover.throttle = -1

    if Rover.vel > abs(0.2):
        Rover.mode = 'forward'

# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        if Rover.mode == 'forward':
            forward_mode(Rover)
        elif Rover.mode == 'stop':
            stop_mode(Rover)
        elif Rover.mode == 'stuck':
            stuck_mode(Rover)
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True

    return Rover

