import math
import configparser


def pixel_to_mm(gripper_height, puck):
    """Converts coordinates in image from pixels to millimeters. This depends on the height the image is taken from"""
    mm_width = 1 * (gripper_height + 70)  # 1 = Conversion number between camera height and FOV
    # Previous conversion number was 0.95
    pixel_to_mm = mm_width / 1280  # mm_width / px_width

    # Convert all positions from pixels to millimeters:
    puck.set_position(puckpos=[x * pixel_to_mm for x in puck.pos])


def transform_position(gripper_rot, puck):
    """Transform coordinate system given by image in OpenCV to coordinate system of work object in RAPID.
    Swap x & y coordinates and rotate by the same amount that the camera has been rotated."""

    # Perform transformations to match RAPID: x -> y, y -> x, x -> -x, y -> -y
    puck.set_position(puckpos=[-puck.pos[1], -puck.pos[0]])

    # Convert from quaternion to Euler angle (we only need z-axis)
    rotation_z_radians = quaternion_to_euler(gripper_rot)
    rotation_z_degrees = -math.degrees(rotation_z_radians)
    # TODO: Check if rotation is positive or negative for a given orientation

    # TODO: Rotate all points in dict, not list:
    """Rotate all points found by the QR scanner.
    Also, adjust the angle of all pucks by using the orientation of the gripper:"""
    puck.set_position(puckpos=
                      [puck.pos[0] * math.cos(rotation_z_radians) + puck.pos[1] * math.sin(rotation_z_radians),
                       -puck.pos[0] * math.sin(rotation_z_radians) + puck.pos[1] * math.cos(rotation_z_radians)])

    puck.set_angle(puckang=puck.ang - rotation_z_degrees)


def get_camera_position(trans, rot):
    """Find the offset between gripper and camera"""

    r = 55  # Distance between gripper and camera
    rotation_z_radians = quaternion_to_euler(rot)
    # TODO: Check if angle should be - or +
    offset_x = r * math.cos(rotation_z_radians)
    offset_y = r * math.sin(rotation_z_radians)

    camera_position = [trans[0] + offset_x, trans[1] + offset_y]  # Gripper position + offset from gripper
    return camera_position


def create_robtarget(gripper_height, gripper_rot, cam_pos, puck, cam_comp=False):
    """Combine all known offsets to make a robtarget on the work object"""

    # Converts puck position from pixels to millimeters

    pixel_to_mm(gripper_height=gripper_height, puck=puck)

    # Transform position depending on how the gripper is rotated
    transform_position(gripper_rot=gripper_rot, puck=puck)

    # Compensate for overshoot in 2D image
    overshoot_comp(gripper_height=gripper_height, puck=puck)

    # TODO: Fix camera compensation
    # Compensate for possibly angled camera
    if not cam_comp:
        camera_compensation(gripper_height=gripper_height, puck=puck)

    # Add the offset from camera to gripper
    puck.set_position(puckpos=[puck.pos[0] + cam_pos[0], puck.pos[1] + cam_pos[1]])


def quaternion_to_euler(quaternion):
    """Convert a Quaternion to Euler angle. We only need the rotation around the z-axis"""
    w, x, y, z = quaternion
    t1 = +2.0 * (w * z + x * y)
    t2 = +1.0 - 2.0 * (y * y + z * z)
    rotation_z = math.atan2(t1, t2)

    return rotation_z


def overshoot_comp(gripper_height, puck):
    """Compensate for the overshoot phenomenon which occurs when trying to pinpoint
    the location of a 3D object in a 2D image"""
    adjustment = [x * 30 / (gripper_height + 70) for x in puck.pos]
    puck.set_position(puckpos=list(map(lambda x, y: x - y, puck.pos, adjustment)))


def camera_compensation(gripper_height, puck):
    """Compensate for an angled camera view. Different cameras will be angled differently both internally and
    externally when mounted to a surface. The slope values must first be calculated by running camera_adjustment.py"""
    camera_height = gripper_height + 70
    # TODO: Run camera_adjustment several times to get an average slope value
    config = configparser.ConfigParser()
    config.read('cam_adjustments.ini')

    slope_x = float(config['SLOPE']['slopex'])
    slope_y = float(config['SLOPE']['slopey'])
    comp_x = slope_x * camera_height
    comp_y = slope_y * camera_height
    puck.set_position(puckpos=[puck.pos[0] - comp_x, puck.pos[1] - comp_y])

