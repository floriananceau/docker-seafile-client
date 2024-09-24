#!/usr/bin/env python3

from pathlib import Path
from typing import Any
import argparse
import logging
import os
import subprocess
import sys
import time

import seafile


class BadConfiguration(Exception):
    pass


def get_configuration(variable: str, *args) -> Any:
    """Helper function to get a configuration.
    see https://gitlab.com/-/snippets/1941025
    """

    # Assign the default value from the first item of *args.
    if args:
        default = args[0]

    # Try to get the variable from a Docker Secret.
    try:
        file = os.environ[f"{variable}_FILE"]
    except KeyError:
        pass
    else:
        with open(file, "rt") as fo:
            return fo.read()

    # Try to get the variable from an environment variable.
    try:
        return os.environ[variable]
    except KeyError:
        pass

    # Try to return the default value,
    # if no default exist, then it is a required variable.
    try:
        return default
    except UnboundLocalError:
        raise BadConfiguration(
            f"Environment variable {variable} was not found but is required."
        )

class Client:

    def __init__(self) -> None:
        # Client configuration
        self.username: str = get_configuration("SEAF_USERNAME")
        self.password: str = get_configuration("SEAF_PASSWORD")
        self.url: str = get_configuration("SEAF_SERVER_URL")
        self.skip_ssl_cert: bool = bool(get_configuration("SEAF_SKIP_SSL_CERT", None))
        self.upload_limit: int = get_configuration("SEAF_UPLOAD_LIMIT", None)
        self.download_limit: int = get_configuration("SEAF_DOWNLOAD_LIMIT", None)
        self.mfa_secret: str = get_configuration("SEAF_2FA_SECRET", None)

        # Paths
        self.ini = Path.home().joinpath(".ccnet", "seafile.ini")
        self.log = Path.home().joinpath(".ccnet", "logs", "seafile.log")
        self.seafile = Path("/seafile")
        self.socket = self.seafile.joinpath("seafile-data", "seafile.sock")
        self.target = Path("/library")

        # Binaries, instances.
        if self.socket.exists():
            self.rpc = seafile.RpcClient(str(self.socket))

        self.binary = ["seaf-cli"]
        self._get_librairies()

    def _get_librairies(self):
        self.libraries = {}

        # Single library use case. Mutually exclusive to mulitple labraries use case.
        single_library_variables = ["SEAF_LIBRARY", "SEAF_LIBRARY_UUID", "SEAF_LIBRARY_PASSWORD"]
        if any(environ in single_library_variables for environ in os.environ):
            logger.info("Single library detected. Multiple libraries will be ignored.")
            library = {}

            # Grab the UUID, usin both the 
            uuid = None
            if legacy := os.getenv("SEAF_LIBRARY_UUID", None):
                logger.warning("SEAF_LIBRARY_UUID is obsolete, please use SEAF_LIBRARY instead.")
                uuid = legacy
            if current := os.getenv("SEAF_LIBRARY", None):
                uuid = current

            # Exit if no UUID was provided, continue otherwise.
            if uuid is None:
                raise Exception("Please provide an UUID with SEAF_LIBRARY for single library usage.")
            library["uuid"] = uuid

            if password := os.getenv("SEAF_LIBRARY_PASSWORD", None):
                library["password"] = password

            # Assign and return a default library.
            self.libraries["_"] = library
            return

        # Multiple libraries use case.
        # Loop over all sorted variables prefixed with SEAF_LIBRARY.
        for variable in sorted(os.environ):
            if variable.startswith("SEAF_LIBRARY"):

                # Get the variable name.
                name = variable.split("_")[2].lower()

                # Read the password as a secret.
                if "_PASSWORD" in variable:
                    password = get_configuration(variable, None)
                    try:
                        if password:
                            self.libraries[name]["password"] = password
                    except KeyError:
                        logger.warning(f"Cannot set a password to unknown library {name}")

                # Or got the name, build the dictionary with the name and uuid.
                else:
                    self.libraries[name] = {}
                    uuid = os.environ[variable]
                    self.libraries[name]["uuid"] = uuid

    def initialize(self):
        # Initialize the Seafile client.
        logger.info("Initializing `seaf-cli`.")
        if not self.ini.exists():
            logger.info("Seafile .ini file not found, running `seaf-cli init`")
            #self.ini.parent.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(self.binary + ["init", "-d", str(self.seafile)])
            while not self.ini.exists():
                logging.debug("Waiting for the .ini file to be created...")
                time.sleep(1)

        # Start the Seafile client.
        logger.info("Starting `seaf-cli`.")
        subprocess.run(self.binary + ["start"])
        while not self.socket.exists():
            logger.debug("Waiting for the Seafile client socket to be created.")
            time.sleep(1)

        self.rpc = seafile.RpcClient(str(self.socket))

    def configure(self):
        command = self.binary + ["config"] 
        if self.skip_ssl_cert:
            subprocess.run(command +["-k", "disable_verify_certificate", "-v", str(self.skip_ssl_cert)])
        if self.download_limit:
            subprocess.run(command +["-k", "download_limit", "-v", self.download_limit])
        if self.upload_limit:
            subprocess.run(command +["-k", "upload_limit", "-v", self.upload_limit])

    def synchronize(self):
        core = self.binary + ["sync", "-u", self.username, "-p", self.password, "-s", self.url]
        for name, configuration in self.libraries.items():
            uuid = configuration["uuid"]

            # Check if repository is already synced.
            repository = self.rpc.get_repo(uuid)
            if repository is not None:
                logger.info(f"Library {name} is already synced.")
                continue

            command = core + ["-l", uuid]

            if "password" in configuration:
                password = configuration["password"]
                command += ["-e", password]
            
            target = self.target if name == "_" else self.target.joinpath(name)
            target.mkdir(parents=True, exist_ok=True)
            command += ["-d", str(target)]

            if self.mfa_secret:
                totp = subprocess.run(
                    f"oathtool --base32 --totp {self.mfa_secret}",
                    text=True,
                    capture_stdout=True).stdout
                command += ["-a", totp]

            logging.debug(f"Running {' '.join(command)}")
            subprocess.run(command)  

    def follow(self):
        logging.debug(f"Running `tail -v -f {self.log}`")
        subprocess.run(["tail", "-v", "-f", self.log])

    def healthcheck(self):

        tasks = self.rpc.get_clone_tasks()
        healthy = True
        for task in tasks:
            name = task.repo_name
            state = task.state

            if task.state == 'done':
                continue
            elif state == "fetch":
                tx_task = self.rpc.find_transfer_task(task.repo_id)
                percentage = 0 if tx_task.block_done == 0 else tx_task.block_done / tx_task.block_total * 100
                rate = 0 if tx_task.rate == 0 else tx_task.rate / 1024.0
                print(f"{name:<50s}\t{state:<20s}\t{percentage:<.1f}%, {rate:<.1f}KB/s")
            elif task.state == "error":
                healthy = False
                error = self.rpc.sync_error_id_to_str(task.error)
                print(f"{name:<50s}\t{state:<20s}\t{error}")
            else:
                print(f"{name:<50s}\t{state:<20s}")

        repos = self.rpc.get_repo_list(-1, -1)
        for repo in repos:
            name = repo.name

            auto_sync_enabled = self.rpc.is_auto_sync_enabled()
            if not auto_sync_enabled or not repo.auto_sync:
                state = "auto sync disabled"
                print(f"{name:<50s}\t{state:<20s}")
                continue

            task = self.rpc.get_repo_sync_task(repo.id)
            if task is None:
                state = "waiting for sync"
                print(f"{name:<50s}\t{state:<20s}")
                continue

            state = task.state
            if state in ['uploading', 'downloading']:
                tx_task = self.rpc.find_transfer_task(repo.id)
                if tx_task.rt_state == "data":
                    state += " files"
                    percentage = 0 if tx_task.block_done == 0 else tx_task.block_done / tx_task.block_total * 100
                    rate = 0 if tx_task.rate == 0 else tx_task.rate / 1024.0
                    print(f"{name:<50s}\t{state:<20s}\t{percentage:<.1f}%, {rate:<.1f}KB/s")
                elif tx_task.rt_state == "fs":
                    state += " files list"
                    percentage = 0 if tx_task.fs_objects_done == 0 else tx_task.fs_objects_done / tx_task.fs_objects_total * 100
                    print(f"{name:<50s}\t{state:<20s}\t{percentage:<.1f}%")
            elif state == 'error':
                healthy = False
                error = self.rpc.sync_error_id_to_str(task.error)
                print(f"{name:<50s}\t{state:<20s}\t{error}")
            else:
                print(f"{name:<50s}\t{state:<20s}")


def entrypoint():
    try:
        logging.debug("Instanciating the client")
        client = Client()
    except BadConfiguration as e:
        logger.error(f"Bad configuration: {e}")
        sys.exit(1)

    logging.debug("Initializing the client")
    client.initialize()
    logging.debug("Configuring the client")
    client.configure()
    logging.debug("Synchronizing the client")
    client.synchronize()
    logging.debug("Following the client")
    client.follow()


debug = get_configuration("DEBUG", False)
level = logging.INFO
format = "%(asctime)s - %(levelname)s - %(message)s"
if debug:
    level = logging.DEBUG
    format = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
logging.basicConfig(format=format, level=level)
logger = logging.getLogger()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="",
        description="",
        epilog=""
    )
    parser.add_argument("--healthcheck", action="store_true")
    args = parser.parse_args()
    healthcheck = args.healthcheck

    if healthcheck:
        logger.disabled = True

    try:
        logging.debug("Instanciating the client")
        client = Client()
    except BadConfiguration as e:
        logger.error(f"Bad configuration: {e}")
        sys.exit(1)

    if healthcheck:
        logging.debug("Running healthchecks")
        sys.exit(client.healthcheck())

    logging.debug("Initializing the client")
    client.initialize()
    logging.debug("Configuring the client")
    client.configure()
    logging.debug("Synchronizing the client")
    client.synchronize()
    logging.debug("Following the client")
    client.follow()

