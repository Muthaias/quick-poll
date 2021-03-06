# Disclaimer
This is not the best code in the world. This is just a tribute. The goal of this project is to try out `Flask`and `SQLAlchemy` as tools to build rest APIs. The final system will be an authentication free service by utilizing signed JWTs to handle authorization.

# QuickPoll
QuickPoll aims to be a simple REST-API which exposes simple public poll functionality. No sign in is required to vote but authenticated tokens are required to create and update polls.
The main features are as follows:
* CRUD public polls
* Vote in public polls
* Get poll results

# To run
To run this system yourself either have a look in the `Dockerfile`, for a hint of what the dependencies are, or just use the `Dockerfile` with `podman` or `Docker`. The scripts `build-container.sh` and `run-container.sh` expects `podman` to be used but they should be easily modifiable to use `Docker` instead.

* Make sure all dependencies are installed on your host OS
* `sh build-container.sh`
* `sh run-container.sh`
* Inside terminal of container:
    * `python create_db.py`
    * `python run.py`


# To configure
The system optionally supports configuration via JSON. The configuration file will be loaded from the execution directory of the system and should be named `./config.json`. The file `config.default.json` contains an example of a working configuration file.