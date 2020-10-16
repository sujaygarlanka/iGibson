""" VR saving demo using simplified VR playground code.

This demo saves to vr_logs/vr_demo_save.h5
If you would like to replay the data, please run
vr_demo_replay using this file path as an input.

Run this demo if you would like to save your own data."""

import numpy as np
import os
import pybullet as p

from gibson2.scenes.gibson_indoor_scene import StaticIndoorScene
from gibson2.objects.articulated_object import ArticulatedObject
from gibson2.objects.vr_objects import VrHand
from gibson2.objects.visual_marker import VisualMarker
from gibson2.objects.ycb_object import YCBObject
from gibson2.simulator import Simulator
from gibson2.utils.vr_logging import VRLogWriter
from gibson2.utils.vr_utils import translate_vr_position_by_vecs
from gibson2 import assets_path
sample_urdf_folder = os.path.join(assets_path, 'models', 'sample_urdfs')

# Playground configuration: edit this to change functionality
optimize = True
vr_mode = True
print_fps = False
# Toggles fullscreen companion window
fullscreen = False
# Toggles SRAnipal eye tracking
use_eye_tracking = True
# Toggles movement with the touchpad (to move outside of play area)
touchpad_movement = True
# Set to one of hmd, right_controller or left_controller to move relative to that device
relative_movement_device = 'hmd'
# Movement speed for touchpad movement
movement_speed = 0.01

# Initialize simulator
s = Simulator(mode='vr', timestep = 1/90.0, optimized_renderer=optimize, vrFullscreen=fullscreen, vrEyeTracking=use_eye_tracking, vrMode=vr_mode)
scene = StaticIndoorScene('Placida')
s.import_scene(scene)

# This playground only uses one hand - it has enough friction to pick up some of the
# mustard bottles
rHand = VrHand()
s.import_object(rHand)
# This sets the hand constraints so it can move with the VR controller
rHand.set_start_state(start_pos=[0.0, 0.5, 1.5])

# Add playground objects to the scene
# Eye tracking visual marker - a red marker appears in the scene to indicate gaze direction
gaze_marker = VisualMarker(radius=0.03)
s.import_object(gaze_marker)
gaze_marker.set_position([0,0,1.5])

basket_path = os.path.join(sample_urdf_folder, 'object_ZU6u5fvE8Z1.urdf')
basket = ArticulatedObject(basket_path)
s.import_object(basket)
basket.set_position([1, 0.2, 1])
p.changeDynamics(basket.body_id, -1, mass=5)

mass_list = [5, 10, 100, 500]
mustard_start = [1, -0.2, 1]
for i in range(len(mass_list)):
    mustard = YCBObject('006_mustard_bottle')
    s.import_object(mustard)
    mustard.set_position([mustard_start[0], mustard_start[1] - i * 0.2, mustard_start[2]])
    p.changeDynamics(mustard.body_id, -1, mass=mass_list[i])

if optimize:
    s.optimize_vertex_and_texture()

# Start user close to counter for interaction
s.setVROffset([1.0, 0, -0.4])

# Modify this path to save to different files
vr_log_path = 'vr_logs/vr_demo_save.h5'
# Saves every 2 seconds or so (200 / 90fps is approx 2 seconds)
vr_writer = VRLogWriter(frames_before_write=200, log_filepath=vr_log_path, profiling_mode=True)

# Save Vr hand transform, validity and trigger fraction
# action->vr_hand (dataset)
# Total size of numpy array: 1 (validity) + 3 (pos) + 4 (orn) + 1 (trig_frac) = (9,)
vr_hand_action_path = 'vr_hand'
vr_writer.register_action(vr_hand_action_path, (9,))

# Call set_up_data_storage once all actions have been registered
vr_writer.set_up_data_storage()

# Main simulation loop - 20 to 30 seconds of simulation data recorded
for i in range(210):
    # Optionally print fps during simulator step
    s.step(shouldPrintTime=print_fps)

    rIsValid, rTrans, rRot = s.getDataForVRDevice('right_controller')
    rTrig, rTouchX, rTouchY = s.getButtonDataForController('right_controller')

    # VR eye tracking data
    is_eye_data_valid, origin, dir, left_pupil_diameter, right_pupil_diameter = s.getEyeTrackingData()
    if is_eye_data_valid:
        # Move gaze marker based on eye tracking data
        updated_marker_pos = [origin[0] + dir[0], origin[1] + dir[1], origin[2] + dir[2]]
        gaze_marker.set_position(updated_marker_pos)

    # Get coordinate system for relative movement device
    right, _, forward = s.getDeviceCoordinateSystem(relative_movement_device)

    # Save VR hand data
    vr_hand_data = [1.0 if rIsValid else 0.0]
    vr_hand_data.extend(rTrans)
    vr_hand_data.extend(rRot)
    vr_hand_data.append(rTrig)
    vr_hand_data = np.array(vr_hand_data)
    
    vr_writer.save_action(vr_hand_action_path, vr_hand_data)

    if rIsValid:
        rHand.move(rTrans, rRot)
        rHand.set_close_fraction(rTrig)
        s.setVROffset(translate_vr_position_by_vecs(rTouchX, rTouchY, right, forward, s.getVROffset(), movement_speed))

    # Record this frame's data in the VRLogWriter
    vr_writer.process_frame(s)

# Note: always call this after the simulation is over to close the log file
# and clean up resources used.
vr_writer.end_log_session()
s.disconnect()