import configparser
import os

def test():
    configfile_name = "image_tools/cam_adjustments.ini"

    Config = configparser.ConfigParser()
    Config.read(configfile_name)

    # Create the configuration file as it doesn't exist yet
    cfgfile = open(configfile_name, 'w')

    # Add content to the file
    Config.set('SLOPE', 'slopex', '5')
    Config.set('SLOPE', 'slopey', '5')

    Config.write(cfgfile)
    cfgfile.close()