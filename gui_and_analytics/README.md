## gui_and_analytics

This Python project is for the development of tools that help with data processing, visualization and analytics

It uses Tkinter for the user interface.

### Getting Started

1. Download PyCharm Professional edition
    - https://www.jetbrains.com/pycharm/download/#section=windows
    - you can get a full license with your student .edu email
    - IMPORTANT: check that you have the Docker plugin installed in PyCharm

2. Download Docker
    - https://docs.docker.com/toolbox/toolbox_install_windows/

3. Download VNC Viewer
    - https://www.realvnc.com/en/connect/download/viewer/

4. Run `./docker_init.sh`

5. Run `./run_desktop.sh`
    - on Mac OS, you may need to go to System Preferences -> Sharing
      and disable screen sharing

6. Open VNC Viewer, and open a client to `127.0.0.1`.
    - when prompted, the password is "password"

7. Within VNC Viewer, right click to bring up the menu
    - Launch Applications->Shells->Bash
    - this desktop is now common among all collaborators
    
8. Try some python scripts
   - `python -m analytics.plots.plot_forecast`
   
9. Stop the desktop
   - in a new bash window (on the host machine) run `./stop_desktop.sh`
   
10. In PyCharm, set up the python interpretter to use Docker
   - Create new Python interpretter
   - Choose Docker
   - Choose image capstone-solar-sailor:latest
   
