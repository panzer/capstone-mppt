
# https://phoenixnap.com/kb/how-to-list-start-stop-docker-containers
# https://docs.docker.com/engine/reference/commandline/ps/
docker stop "$(docker ps -f ancestor=capstone-solar-sailor -l -q)"