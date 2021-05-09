import numpy as np
import os

import gibson2
from gibson2 import object_states
from gibson2.simulator import Simulator
from gibson2.scenes.empty_scene import EmptyScene
from gibson2.objects.ycb_object import YCBObject
from gibson2.objects.articulated_object import URDFObject
from gibson2.utils.assets_utils import get_ig_model_path
from gibson2.object_states.factory import prepare_object_states



def main():
    s = Simulator(mode='iggui', image_width=1280,
                  image_height=720)

    scene = EmptyScene()
    s.import_scene(scene)

    model_path = os.path.join(get_ig_model_path('sink', 'sink_1'), 'sink_1.urdf')

    sink = URDFObject(filename=model_path,
                      category='sink',
                      name='sink_1',
                      scale=np.array([0.8, 0.8, 0.8]),
                      abilities={'toggleable': {}, 'waterSource': {}}
                      )

    s.import_object(sink)
    sink.set_position([1, 1, 0.8])
    sink.states[object_states.ToggledOn].set_value(True)

    block = YCBObject(name='036_wood_block')
    block.abilities = ["soakable", "cleaning_tool"]
    prepare_object_states(block, abilities={"soakable": {}, "cleaning_tool": {}})
    s.import_object(block)
    block.set_position([1, 1, 1.8])
    # assume block can soak water

    model_path = os.path.join(get_ig_model_path('breakfast_table', '19203'), '19203.urdf')
    desk = URDFObject(filename=model_path,
                      category='table',
                      name='19898',
                      scale=np.array([0.8, 0.8, 0.8]),
                      abilities={'stainable': {}}
                      )

    print(desk.states.keys())
    s.import_object(desk)
    desk.set_position([1, -2, 0.4])
    s.step()
    desk.states[object_states.Stained].set_value(True)

    # Main simulation loop
    try:
        while True:
            s.step()
    finally:
        s.disconnect()


if __name__ == '__main__':
    main()