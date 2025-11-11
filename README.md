# cps-cosimulation-env
## Pre-requisites
Must have Git and Docker installed. The steps to install Docker for different operating systems are given below.
- MacOS - follow the instructions [here](https://docs.docker.com/desktop/setup/install/mac-install/).
    - Follow the steps for "Mac with Apple silicon." Make sure to install Rosetta 2. Once installed, open Docker Desktop, click the Docker icon in the macOS menu bar and select "Settings." Navigate to General Settings, then enable Rosetta Emulation by checking "Use Virtualization Framework" and "Use Rosetta for x86/amd64 emulation on Apple Silicon." Click Apply & Restart" to save the changes.
- Windows - follow the instructions [here](https://docs.docker.com/desktop/setup/install/windows-install/).
   - Follow the steps for WSL 2 backend, and follow the directions for installing Docker Desktop interactively.
- Linux - you should know what you're doing.

To verify that Docker is working properly, run `docker info` from the command line. If you don't see any errors (such as `Cannot connect to Docker daemon`), you are good to move on.

## Installation Steps
1. Clone this repo: `git clone https://github.com/cps-vip/cps-cosimulation-env.git`
2. Go into the repo: `cd cps-cosimulation-env`
3. Switch to the Networking_team branch: `git switch Networking_team`
4. Update the Git submodules: `git submodule update --init --recursive`
5. Build the Docker image: `docker build --platform=linux/amd64 -t cps-cosimulation-env:latest .`
6. Run the Docker container: `docker run -it --rm --name cps-vip --platform linux/amd64 -v .:/home/vip/cps-cosimulation-env cps-cosimulation-env:latest /bin/bash`
7. Run the one-time setup script: `./setup.sh`. Warning - this will take a long time.

## Post-Install Steps
The two important top-level directories are `simple_gridlabd_example`, which is an example of HELICS and Gridlab-D, and `device_modeling`, which represents the substation simulation. The following steps should be ran while in the Docker container shell. If you are following from the previous installation steps, you are already in the Docker container shell. Otherwise, navigate to the `cps-cosimulation-env` directory and run `docker run -it --rm --name cps-vip --platform linux/amd64 -v .:/home/vip/cps-cosimulation-env cps-cosimulation-env:latest /bin/bash`. This `docker run` command will be necessary whenever you want to work on the project.

### Running `simple_gridlabd_example`
```bash
# Enable the Python virtual environment created by setup.sh
cd ~/cps-cosimulation-env
source .venv/bin/activate
cd simple_gridlabd_example

# This will take a while
./run_example.sh

# To verify everything worked, look at the logs in the results directory
# Check that the outputs looks reasonable (no errors)
```

### Running `device_modeling`
```bash
cd ~/cps-cosimulation-env/device_modeling/src

# This is just a very verbose version of the command "python run_simulation.py"
PYTHON_GIL=0 uv run --python 3.14t --reinstall-package dnp3 run_simulation.py

# To verify the results, look at simulation.log. There should be no obvious errors.
# The last line should say "INFO:__main__:Co-simulation completed."
cat simulation.log

# Try out the DNP3 example as well. The last line of simulation.log should be:
# "INFO:master:runtime shutdown complete"
rm simulation.log
PYTHON_GIL=0 uv run --python 3.14t --reinstall-package dnp3 run_dnp3_demo.py
cat simulation.log
```

## VS Code Integration
If you are using VS Code, the `Dev Containers` extension will allow you to get proper syntax highlighting and LSP integration.

Steps:
1. If not already done, start a terminal in the Docker container shell (using the same `docker run` command from the installation steps)
2. Install the `Dev Containers` extension in VS Code
3. Click on the button on the very bottom left
4. Now near the top middle, click `Attach to Running Container`. You will likely get some warning about executing arbitrary code, just click accept and move on.
5. Click on the `cps-vip` line. This will open a new VS Code window in the Docker container. You are free to close the old window.
6. Open the file explorer (button near the top left) and click `Open Folder`. From the dropdown, select the `cps-cosimulation-env` directory (the bottom entry), then click `OK`
7. Install the C/C++ Extension Pack. If you see pop-ups asking about CMakeLists.txt or Kits, just select the first option both times.
8. To verify everything worked, navigate to the file `python-dnp3/src/dnp3/master.c` and open it. After a bit of processing, you should see nice syntax highlighting and IntelliSense working.

Note that the Docker container started in step 1 must continue running in the background. If you stop the container, VS Code will get disconnected.

After doing these steps once, you should only need to do steps 1, 3, 4, and 5 to get back to the same place.

## Development Workflow
After following all the previous installation steps, you can reference this section going forward. Whenever you want to start working on the project, perform the following steps:
1. Open a terminal able to run Docker commands
2. Change directory to the directory containing this repo (cps-cosimulation-env)
3. Run `docker run -it --rm --name cps-vip --platform linux/amd64 -v .:/home/vip/cps-cosimulation-env cps-cosimulation-env:latest /bin/bash`
4. If using VS Code, click on the button on the very bottom left -> `Attach to Running Container` -> `cps-vip`
5. To run the substation simulation, run the following commands in the terminal opened in step 1:
```bash
cd device_modeling/src

# If the Python dnp3 library hasn't been modified (so you aren't on the networking subteam):
python run_simulation.py

# If you are working on the Python dnp3 library (so you are on the networking subteam):
uv run --reinstall-package dnp3 run_simulation.py

# Regardless of which command you can above, the results will be in simulation.log
# You can also view the log in VS Code instead
cat simulation.log
```

