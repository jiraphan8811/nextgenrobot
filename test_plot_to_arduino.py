import sys
import math
import matplotlib.pyplot as plt
import serial
import time

# Serial setup (adjust the port and baud rate as needed)
arduino = serial.Serial(port='COM11', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port

# Constants
l0 = 50  # Length between origin and the two motors
l1 = 50  # Length from motor to passive joints
l2 = 102.225  # Length from passive joints to end effector

def calc_angles(x, y):
    # Angle from left shoulder to end effector
    beta1 = math.atan2(y, (l0 + x))

    # Angle from right shoulder to end effector
    beta2 = math.atan2(y, (l0 - x))

    # Alpha angle pre-calculations
    alpha1_calc = (l1**2 + ((l0 + x)**2 + y**2) - l2**2) / (2 * l1 * math.sqrt((l0 + x)**2 + y**2))
    alpha2_calc = (l1**2 + ((l0 - x)**2 + y**2) - l2**2) / (2 * l1 * math.sqrt((l0 - x)**2 + y**2))

    # If calculations > 1, will fail acos function
    if alpha1_calc > 1 or alpha2_calc > 1:
        print("Unreachable coordinates")
        return None

    # Angle of left shoulder - beta1 and right shoulder - beta2
    alpha1 = math.acos(alpha1_calc)
    alpha2 = math.acos(alpha2_calc)

    # Angles of left and right shoulders
    shoulder1 = math.degrees(beta1 + alpha1)
    shoulder2 = math.degrees(math.pi - beta2 - alpha2)
    
    return shoulder1, shoulder2

def plot_arms(shoulder1, shoulder2, efx, efy):
    # Passive joints (x, y) location
    p1 = (-l0 + l1 * math.cos(math.radians(shoulder1)), l1 * math.sin(math.radians(shoulder1)))
    p2 = (l0 + l1 * math.cos(math.radians(shoulder2)), l1 * math.sin(math.radians(shoulder2)))

    # Left arm
    plt.plot([-l0, p1[0], efx], [0, p1[1], efy], 'bo-')
    plt.text(-l0 + 0.3, 0 + 0.3, "{:.2f} degrees".format(shoulder1))
    plt.text(p1[0] + 0.3, p1[1] + 0.3, "({:.2f}, {:.2f})".format(p1[0], p1[1]))

    # Right arm
    plt.plot([l0, p2[0], efx], [0, p2[1], efy], 'bo-')
    plt.text(l0 + 0.3, 0 + 0.3, "{:.2f} degrees".format(shoulder2))
    plt.text(p2[0] + 0.3, p2[1] + 0.3, "({:.2f}, {:.2f})".format(p2[0], p2[1]))

    # EF
    plt.plot(efx, efy, 'ro')
    plt.text(efx + 0.3, efy + 0.3, "({:.2f}, {:.2f})".format(efx, efy))

def plot_plot(efx, efy):
    plt.title('5-Bar Parallel Robot Kinematics')
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.grid(True)

    angles = calc_angles(efx, efy)
    if angles is not None:
        s1, s2 = angles
        plot_arms(s1, s2, efx, efy)
        send_to_arduino(s1, s2)  # Send the angles to Arduino
    plt.draw()
    plt.pause(0.01)
    plt.clf()

def send_to_arduino(s1, s2):
    """ Send motor angles to Arduino via serial communication. """
    data = "{:.2f},{:.2f}\n".format(s1, s2)  # Format as a string "s1,s2"
    arduino.write(data.encode())  # Send to Arduino

if __name__ == "__main__":
    while True:
        try:
            x = float(input("Enter x coordinate: "))
            y = float(input("Enter y coordinate: "))
            plot_plot(x, y)
        except ValueError:
            print("Please enter valid numeric values for x and y.")
        except KeyboardInterrupt:
            arduino.close()  # Close the serial connection before exiting
            break
