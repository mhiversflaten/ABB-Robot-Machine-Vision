import numpy as np
from RobotWare import RAPID
from config import config
from image_tools import ImageFunctions
import configparser
import os

norbert = RAPID.RAPID()  # Initialize robot communication
norbert.request_mastership()  # Request mastership
norbert.start_RAPID()  # NB! Starts RAPID execution from main
norbert.wait_for_rapid()

cam_comp = True
cam = config.cam

adjustment_file = open('camera_adjustment_XS.txt', 'w')

while norbert.is_running():
    norbert.set_rapid_variable("WPW", 5)  # Start camera adjustment procedure in RAPID

    norbert.wait_for_rapid()

    robtarget_pucks = []

    while not robtarget_pucks:
        ImageFunctions.findPucks(cam, norbert, robtarget_pucks, cam_comp=cam_comp)

    norbert.set_robtarget_translation("puck_target", robtarget_pucks[0].get_xyz())
    norbert.set_rapid_variable("image_processed", "TRUE")

    robtarget_pucks.clear()

    norbert.wait_for_rapid()

    while not robtarget_pucks:
        ImageFunctions.findPucks(cam, norbert, robtarget_pucks, cam_comp=cam_comp)

    norbert.set_rapid_variable("image_processed", "TRUE")

    pos_low = robtarget_pucks[0].get_xyz()
    print(f'Low robtarget: ({pos_low[0]:.1f},{pos_low[1]:.1f})')

    norbert.wait_for_rapid()

    robtarget_pucks.clear()
    while not robtarget_pucks:
        ImageFunctions.findPucks(cam, norbert, robtarget_pucks, cam_comp=cam_comp)

    pos_high = robtarget_pucks[0].get_xyz()
    print(f'High robtarget: ({pos_high[0]:5.1f},{pos_high[1]:5.1f})')

    delta_h = 500 - 60
    delta_x = pos_high[0] - pos_low[0]
    delta_y = pos_high[1] - pos_low[1]
    print(f'Delta: ({delta_x:5.1f}, {delta_y:5.1f})')

    slope_x = delta_x / delta_h
    slope_y = delta_y / delta_h

    if cam_comp and norbert.is_running():
        adjustment_file.write(f'{slope_x:.4f},{slope_y:.4f}\n')

adjustment_file.close()

contents = np.genfromtxt(r'camera_adjustment_XS.txt', delimiter=',')
os.remove('camera_adjustment_XS.txt')

sum_slope_x = 0
sum_slope_y = 0
for content in contents:
    sum_slope_x += abs(content[0])
    sum_slope_y += abs(content[1])

average_slope_x = sum_slope_x / len(contents)
average_slope_y = sum_slope_y / len(contents)

"""Testing file for initializing values for the *.ini files. Method can be used in other configuration files to save
values to """

configfile_name = "cam_adjustments.ini"

Config = configparser.ConfigParser()
Config.read(configfile_name)

# Create the configuration file as it doesn't exist yet
cfgfile = open(configfile_name, 'w')

# Add content to the file
Config.set('SLOPE', 'slopex', f'{average_slope_x:.4f}')
Config.set('SLOPE', 'slopey', f'{average_slope_y:.4f}')

Config.write(cfgfile)
cfgfile.close()
