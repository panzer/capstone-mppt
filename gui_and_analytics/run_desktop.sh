
# Start the Debian desktop
# Will need to figure out USB devices in the future:
# https://stackoverflow.com/questions/24225647/docker-a-way-to-give-access-to-a-host-usb-or-serial-device
docker run -p 5900:5900 -e VNC_SERVER_PASSWORD=password -v "/$(pwd):/app" capstone-solar-sailor:latest