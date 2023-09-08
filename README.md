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
        - If you're not sure how to do this, running something like `sudo nano /etc/nix/nix.conf` should get you there. If you're stuck in terminal text editors, refer to the following links:
            - [Nano](https://www.freecodecamp.org/news/how-to-save-and-exit-nano-in-terminal-nano-quit-command/)
            - [Vim](https://saturncloud.io/blog/how-do-i-exit-the-vim-editor/)
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
    ```
    cd HELICS
    mkdir build
    cd build

    cmake ../ -DCMAKE_INSTALL_PREFIX=../../install -DCMAKE_CXX_EXTENSIONS=ON -DHELICS_BUILD_CXX_SHARED_LIB=ON

    make
    make install
    cd ../ # This takes us back to the cps-cosimulation-env directory
    ```
6. Build Gridlab-D
    - Now we'll follow a very similar process for gridlab-d
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

# Troubleshooting

Here are some problems we've run into in the past, and solutions that have solved those problems.

## Not finding build tools

If you get an error like `cmake: command not found` while following the above readme, it's possible your `nix` installation didn't correctly complete. Try to following to verify you're in the correct `nix` environment:

```
which cmake
# If not in nix, this will either show something like /usr/bin/local/cmake or "cmake not found" depending on whether cmake is installed outside of nix
# If you correctly installed and "nix develop" dropped you into our build environment, you should get something like:
# /nix/store/08nrfzzy1jamc21qj6pfrcn0q2h334bl-cmake-3.26.4/bin/cmake
```

Verify that your nix was installed with the correct permissions and that you're running `nix develop` within the `cps-cosimulation-env` folder. If both those are true and `which cmake` still doesn't point to `/nix`, please let us know!

## Nix has permission errors when first running `nix develop`

If you run `nix develop` and encounter an error such as:

`error: could not set permissions on '/nix/var/nix/profiles/per-user' to 755: Operation not permitted`

Nix might have been installed with incorrect flags. One cause of this is following the Mac/Linux Nix installation when on WSL2, where the `--daemon` flag is causing the error. Double check the installation command on Nix's official website here: `https://nixos.org/download`.