# cps-cosimulation-env

## Clean Install on M2 Mac
The following list of steps details a clean install of the required dependencies to run this simulation on a modern M2 aarch64 Mac.

1. Install nix
    - In `terminal`, run `$ sh <(curl -s -L https://nixos.org/nix/install) --daemon`
        - We use `nix` as a development shell to make builds as reproducible as possible.
        - This is similar to the default requested installation method found on `https://nixos.org/nix/install`, but gets around a cURL bug where cURL returns `curl: (23) Failed writing body`. The difference is the inserted `-s` flag to the curl call.
        - Follow the prompts that the nix instlalation script gives you, including authorizing sudo access. If desired, you can get it to get step by step authorization, as generally piping a script from curl and running super-user commands is frowned upon! This one's trustworthy though.
    - Now that `nix` is installed, you might have to restart the terminal to access the installed commands. You can either restart the entire window or simply run `$ zsh` to get a new, nested shell.
2. Create a place for us to install build artifacts to
    - In order to setup our environment, we want to have made a folder for our simulations and other built tools to live. As part of the next step, we'll automatically add that folder to the list of places your terminal looks when trying to run binaries or scripts.
    - From within this repository, create the `install/bin` folder. One way to do this is (from the terminal):
        `mkdir -p ./install/bin`
3. Set up the nix development environment
    - `nix` is now installed, and we want to be able to run `nix develop` from inside the class repo to get all our tools built per the instructions in `flake.nix`
    - In a base `nix` install though, `nix develop` is an "experimental feature", and we'll need to enable it in our `nix.conf`
    - To do this, edit `/etc/nix/nix.conf` in your favorite text editor (you might need sudo perms)
    - Add the following line verbatim to the file, anywhere is fine
        `experimental-features = nix-command develop flakes`
    - Now, within the folder this `README.md` and `flake.nix` are in, run `nix develop`, which will fetch a variety of compilation tools and libraries
4. Pull all the listed submodules
    - Currently, if you've only cloned this repo, the `gridlab-d`, `HELICS`, and `HELICS-Examples` directories are empty.
    - This is because those directories are actually git submodules, or other git repositories, and we need to clone them!
    - From inside this directory, run the following commands to initialize and update the git submodules:
        - `git submodule update --init --recursive`
5. Build HELICS
    - Now we have the build tooling and have pulled all our source, so it's time to start building our dependencies
    - First we'll tackle HELICS
    - `cd` into the HELICS subdirectory, and follow the `CLASS_README.md` file found in that folder.
6. Build Gridlab-D
    - Now we'll follow a very similar process for gridlab-d, but we spell it out here since we don't currently have a class-specific setup guide
    ```
    *from the cps-cosimulation-env directory*
    cd gridlab-d
    mkdir build
    cd build
    cmake ../ -DCMAKE_INSTALL_PREFIX=../../install -DGLD_USE_HELICS=ON
    make
    make install
    # TODO: this build currently fails due to errors on `finite`/`isfinite`
    ```