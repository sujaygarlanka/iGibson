# Gibson in VR

Instructions for installing Gibson and VR integration on Windows 10.
Assuming a fresh install of Windows.

These instructions partially overlap with installing Gibson
http://svl.stanford.edu/gibson2/docs/installation.html#installation-method 
but are tailored to run the VR components in Windows.


VR Station
==========

Install Steam, Steam VR, Connect VR headset and base stations, set up VR room
Run steam performance test.

https://www.vive.com/eu/support/vive/category_howto/setting-up-for-the-first-time.html


Dependencies and environment:
=============================

* git 
https://git-scm.com/download/win

* Python
https://www.python.org/downloads/release/python-377/

* Anaconda 
https://www.anaconda.com/distribution/#download-section

Make sure anaconda is added to the PATH as follows:
C:\Users\C\anaconda3
C:\Users\C\anaconda3\Scripts
C:\Users\C\anaconda3\Library\bin

Lack of the later produced error:
HTTP 000 CONNECTION FAILED for url <https://repo.anaconda.com/pkgs/main/win-64/current_repodata.json> Elapsed

* Build Tools for Visual Studio:
Microsoft Visual C++ 14.0 is required. Get it with "Build Tools for Visual Studio": 
https://visualstudio.microsoft.com/downloads/
This is needed for bullet

* cmake:
https://cmake.org/download/
Needed for  GLFWRendererContext, VRUtils, CGLUtils


Gibson
======

* Get codebase and assets:

```
$ git clone git@github.com:fxia22/gibsonv2.git
$ cd gibsonv2
$ git checkout vr
$ git submodule update --init --recursive
```

Download openvr from https://github.com/ValveSoftware/openvr and place it in a folder called openvr in core/render

After this you should have content at:
core/render/glfw
core/render/pybind11

Download Gibson assets and copy to gibsonv2/gibson2/assets/
Download enviroments (scenes) and copy to gibsonv2/gibson2/assets/dataset

* Create anaconda env:

```
$ conda create -n gibsonvr python=3.6
```
Activate conda env:
```
$ activate gibsonvr
```

* Install Gibson in anaconda env:
```
$ cd gibsonv2
```
- If you followed the instructions, gibsonv2 is at the vr branch
```
$ pip install -e .
```

Should end printing 'Successfully installed gibson2'

* Run ohopee demo:

$ python test_vr_renderer_ohopee.py

Other notes
===========
Use \ instead of / in paths on Windows! For example use assets\datasets instead of assets/datasets

Have vr fun!