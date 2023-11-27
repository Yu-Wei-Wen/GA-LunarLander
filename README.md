## System Requirement

### Prepare for Windows

1. Download Swig from [HERE](http://prdownloads.sourceforge.net/swig/swigwin-4.1.1.zip)
    * Extract zipped files to `"C:/swigwin/"`
    * Add `"C:/swigwin/"` to "path" in environmental variable

2. Download MS Build Tools from [HERE](https://visualstudio.microsoft.com/zh-hant/visual-cpp-build-tools/)
3. Run installer, make sure you have ticked
    * MSVC v143 - VS 2022 C++ ...
    * Windows 10 SDK (...) or Windows 11 SDK (...)
    ![MS Build Tools Installer](./img/MS%20Build%20Tools.png)

### Prepare for macOS

1. Install `homebrew` (see https://brew.sh/)
1. Install `swig`

    > `brew install swig`

### Required Python Packages

1. Check your Python version (3.10 recommended). If you need to change Python version,
   a. uninstall your current Python
   b. download Python 3.10 from [HERE](https://www.python.org/downloads/)
2. Install packages

    > `pip install swig`

    > `pip install gymnasium[box2d]`

### Miscellaneous

If you occur an ImportError like `"ImportError: Can't find framework /System/Library/Frameworks/OpenGL.framework."`, please run the following installation.

    > `pip install pyglet==1.5.11`

## Game Details
Landing pad is always at coordinates (0,0). Coordinates are the first two numbers in state vector. Reward for moving from the top of the screen to landing pad and zero speed is about 100..140 points. If lander moves away from landing pad it loses reward back. Episode finishes if the lander crashes or comes to rest, receiving additional -100 or +100 points. Each leg ground contact is +10. Firing main engine is -0.3 points each frame. Solved is 200 points. Landing outside landing pad is possible. Fuel is infinite, so an agent can learn to fly and then land on its first attempt. Action is two real values vector from -1 to +1. First controls main engine, -1..0 off, 0..+1 throttle from 50% to 100% power. Engine can't work with less than 50% power. Second value -1.0..-0.5 fire left engine, +0.5..+1.0 fire right engine, -0.5..0.5 off.