# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


<!-- To log a new version, copy, uncomment, add your changes, then add the tag shortcut at the end of the file -->
<!-- tag --/>
## [tag]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

[tag]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/tag
<!-- /tag --/>

<!-- 3.3.0 -->
## [3.3.0]
### Modified
* Add TARGET environment variable to Makefile commands.
### Fixed
* Fix the TypeError for the skip SSL certificates parameters.

[3.3.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.3.0
<!-- /3.3.0 -->

<!-- 3.2.5 -->
## [3.2.5]
### Modified
* Use CI/CD environment variables for the Docker Hub short description
### Fixed
* The file name used for the Docker Hub full description

[3.2.5]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.2.5
<!-- /3.2.5 -->

<!-- 3.2.4 -->
## [3.2.4]
### Added
* Publish to the new flrnnc/seafile-client repository.
* Write notices regarding the Docker repository move.
### Changed
* Use new CI/CD variables.
* Do not run pipelines on Draft MR. (#69)
### Removed
* Remove the changelog from the Seafile documentation.

[3.2.4]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.2.4
<!-- /3.2.4 -->


## [3.2.3] - 2024/06/27
### Changed
- Update the build badge date on builds. (#61)

[3.2.3]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.2.3
<!-- /3.2.3 -->

## [3.2.2] - 2024/06/09
### Fixed
- Allow the latest tag to be applied to the v9 versions. (#54)
- Restricted SAST jobs to approved pipelines. (#58)

[3.2.2]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.2.2
<!-- /3.2.2 -->

## [3.2.1] - 2024/06/09
### Added
- Merge requests pipeline only runs when merge request has been approved.
### Changed
- Badges are rendered from the Gitlab project itself, not from code. (#62)

[3.2.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.2.1
<!-- /3.2.1 -->

## [3.2.0] - 2024/06/06
### Changed
- Changed the group _users_ GID from 100 to 90. This allow to use the GID 100. (#64)

[3.2.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.2.0
<!-- /3.2.0 -->

## [3.1.0] - 2024/06/02
### Changed
- Disable pipelines on approved merge requests
### Fixed
- Instanciate the RPC client at the initialization (#63)

[3.1.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.1.0
<!-- /3.1.0 -->

## [3.0.1] - 2024/05/27
### Added
* New script to schedule the best possible time to run the build. It relies on WattTime Load Shift feature (#56)
* Weekly build through pipeline schedules. (#56)
### Changed
* Every links pointing to the previous repository flwgns-docker/seafile-client are pointing now to flrnnc-oss/docker-seafile-client. (#56)

[3.0.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.0.1
<!-- /3.0.1 -->

## [3.0.0] - 2024/03/16
### Added
- Support for multiple libraries synchronization (#44, #43, #41)
- Support for Docker Secrets (#25)
- Support for Seafile client's version through Docker tags (#9)
- Build documentation with Jinja2 templates (#42)
- Manage the project with a Makefile (#38)
- Mock Seafile server for testings (#6)
### Changed
- Revised project layout and workflow (#38, #39)
### Fixed
- Fixed the Docker Hub description publish through their API (#10)
- Add ca-certificates and gnupg to support more HTTP certificates (#24)

[3.0.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/3.0.0
<!-- /3.0.0 -->

## [2.2.0] - 2022/08/26
- Update from Debian Buster to Debian Bullseye (!7)
- Improved Seafile apt source installation (!7)

## [2.1.1] - 2020/03/10
- Prevent re-initialization and re-synchronization of the container if it's life cycle change but is not deleted (#14)
## [2.1.0] - 2020/01/30
- Replace previous Bash script that parse `seaf-cli status` with a Python script that use pysearpc to run checks (#13)
- Implement a workaround to probable issue, waiting for the issue to appear (#14)

## [2.0.3] - 2020/01/14
- Read [the docs](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg) a bit more (#5)
## [2.0.2] - 2020/01/14
- Propagate the CI_COMMIT_TAG and CI_PROJECT_URL environment variables into the Dockerfile as [the docs states](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg) (#5)
## [2.0.1] - 2020/01/14
- Update chown path to library, comment chown to an obsolete healthcheck.sh (#11)
- Pass $CI_PROJECT_URL to the Dockerfile as a build argument (#5)
## [2.0.0] - 2020/01/06
- Support 2FA authentication through `oathtool` using the secret key
- Support for upload/download limits
- Support for Seafile library password
- Allow skipping SSL certificates verifications
- Drop Bash/supervisord/cron implementations in favor of showing seafile's log
- Implement basic integration tests that check expected binairies
- Improve continuous integration though splitted jobs
- Revise README
- Change the volume path from /volume to /library for consistency

## [1.2.1] - 2019/12/29
- Switch base image from Debian oldoldstable Jessie to Debian stable Buster to fix unmet dependencies of `seafile-cli` to `python-future` and `python-searpc` (#4)
- Replace `;` with `&&` as commands separators in the Dockerfile's `RUN` to properly report failed commands at CI (#4)
## [1.2.0] - 2019/05/02
- Replace _supervisord_ with _cron_ for running the front job that keeps the container up. It uses less resources.
- Improve the infinite-seaf-cli-start.sh into seafile-healthcheck.sh. The Seafile daemon will not be restarted if it's state are either _downloading_ or _committing_, which otherwise is problematic.

## [1.1.2] - 2019/04/18
- Slim down the Docker image, from 102MB to 67MB, gaining 35MB, reducing size by 34%.
## [1.1.1] - 2019/04/18
- Because of the infinite-seaf-cli-start loop, within the container was running many seaf-daemons. Now, the infinite loop stop the current seaf-daemon before starting it again. (see #3)
## [1.1.0] - 2019/04/09
- The container now actually use the UID/GID provided to it:  
The container entrypoint is run with root, then another entrypoint is run by the container's user, seafuser, to run the Seafile client.

## [1.0.6] - 2019/03/25
- More minor fixes from v1.0.4
## [1.0.5] - 2019/03/25
- Minor fixes from v1.0.4
## [1.0.4] - 2019/03/25
- Fix the build target detection (@a52559ddb38a64d7fceaa8bf9b8afd7356ccc439)
- Login to the Docker Hub from within the script, not the gitlab-ci.yml, using (@72bab017c1167b8ab35cef3cc709ff83686eaca4, @f69483354a4cf8afdbea89ef2bb1d9a9b7b2ac10)
- Require Bash on all Gitlab CI stages (@72bab017c1167b8ab35cef3cc709ff83686eaca4)
- Add a script to push the README.md into the Docker Hub repository's full_description (@8cb49cbc8253368701d718c2e38017790c78ceca, @ca6128fb96602da71f3b7a560e834d1b7587abac)
## [1.0.3] - 2019/03/19
- Restrict staging pipelines to pushed pipelines
- Restrict production pipelines to pushed and triggered pipelines
- Require a build target on triggered production pipelines
## [1.0.2] - 2019/03/18
- Fix a minor issue when testing for requested production build.
## [1.0.1] - 2019/03/18
- Add failsafe when importing Seafile's APT-key
- Restrict production build to latest, majors, minors and revisions version, on-demand.
## [1.0.0] - 2019/03/15
- Release to Docker Hub

## [0.9.2] - 2019/03/15
- Test release on GitLab, before Docker Hub

[2.2.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.2.0
[2.1.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.1.1
[2.1.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.1.0
[2.0.3]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.0.2
[2.0.2]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.0.2
[2.0.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.0.1
[2.0.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/2.0.0
[1.2.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.2.1
[1.2.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.2.0
[1.1.2]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.1.2
[1.1.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.1.1
[1.1.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.1.0
[1.0.6]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.6
[1.0.5]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.5
[1.0.4]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.4
[1.0.3]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.3
[1.0.2]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.2
[1.0.1]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.1
[1.0.0]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/1.0.0
[0.9.2]: https://gitlab.com/flrnnc-oss/docker-seafile-client/-/releases/0.9.2
