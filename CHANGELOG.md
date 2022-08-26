- Close #16: add a templater for Docker Hub and Seafile's forum topic description

## __[2.2.0](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.2.0)__ | _2022/08/26_
- Update from Debian Buster to Debian Bullseye
- Improved Seafile apt source installation

### __[2.1.1](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.1.1)__ | _2020/03/10_
- Close #14: prevent re-initialization and re-synchronization of the container if it's life cycle change but is not deleted
## __[2.1.0](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.1.0)__ | _2020/01/30_
- Close #13: replace previous Bash script that parse `seaf-cli status` with a Python script that use __pysearpc__ to run checks
- Ongoing #14: implement a workaround to probable issue, waiting for the issue to appear

### __[2.0.3](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.0.2)__ | _2020/01/14_
- Close #5:  read [the docs](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg) a bit more.
### __[2.0.2](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.0.2)__ | _2020/01/14_
- Ongoing #5: propagate the CI_COMMIT_TAG and CI_PROJECT_URL environment variables into the Dockerfile as [the docs states](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg).
### __[2.0.1](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.0.1)__ | _2020/01/14_
- Fix #11: update chown path to library, comment chown to an obsolete healthcheck.sh.
- Ongoing #5: pass $CI_PROJECT_URL to the Dockerfile as a build argument. 
# __[2.0.0](https://gitlab.com/flwgns-docker/seafile-client/-/tags/2.0.0)__ | _2020/01/06_
- Support 2FA authentication through `oathtool` using the secret key
- Support for upload/download limits
- Support for Seafile library password
- Allow skipping SSL certificates verifications
- Drop Bash/supervisord/cron implementations in favor of showing seafile's log
- Implement basic integration tests that check expected binairies
- Improve continuous integration though splitted jobs
- Revise README
- Change the volume path from /volume to /library for consistency

### __[1.2.1](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.2.1)__ | _2019/12/29_
- Fix #4:
  - Switch base image from Debian oldoldstable Jessie to Debian stable Buster to fix unmet dependencies of `seafile-cli` to `python-future` and `python-searpc`
  - Replace `;` with `&&` as commands separators in the Dockerfile's `RUN` to properly report failed commands at CI
## __[1.2.0](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.2.0)__ | _2019/05/02_
- Replace _supervisord_ with _cron_ for running the front job that keeps the container up. It uses less resources.
- Improve the __infinite-seaf-cli-start.sh__ into __seafile-healthcheck.sh__. The Seafile daemon will not be restarted if it's state are either _downloading_ or _committing_, which otherwise is problematic.

### __[1.1.2](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.1.2)__ | _2019/04/18_
- Slim down the Docker image, from 102MB to 67MB, gaining 35MB, reducing size by 34%.
### __[1.1.1](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.1.1)__ | _2019/04/18_
- Because of the infinite-seaf-cli-start loop, within the container was running many seaf-daemons. Now, the infinite loop stop the current seaf-daemon before starting it again. (see #3)
## __[1.1.0](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.1.0)__ | _2019/04/09_
- The container now actually use the UID/GID provided to it:  
The container entrypoint is run with root, then another entrypoint is run by the container's user, seafuser, to run the Seafile client.

### __[1.0.6](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.6)__ | _2019/03/25_
- More minor fixes from v1.0.4
### __[1.0.5](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.5)__ | _2019/03/25_
- Minor fixes from v1.0.4
### __[1.0.4](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.4)__ | _2019/03/25_
- Fix the build target detection (@a52559ddb38a64d7fceaa8bf9b8afd7356ccc439)
- Login to the Docker Hub from within the script, not the gitlab-ci.yml, using (@72bab017c1167b8ab35cef3cc709ff83686eaca4, @f69483354a4cf8afdbea89ef2bb1d9a9b7b2ac10)
- Require Bash on all Gitlab CI stages (@72bab017c1167b8ab35cef3cc709ff83686eaca4)
- Add a script to push the README.md into the Docker Hub repository's full_description (@8cb49cbc8253368701d718c2e38017790c78ceca, @ca6128fb96602da71f3b7a560e834d1b7587abac)
### __[1.0.3](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.3)__ | _2019/03/19_
- Restrict staging pipelines to pushed pipelines
- Restrict production pipelines to pushed and triggered pipelines
- Require a build target on triggered production pipelines
### __[1.0.2](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.2)__ | _2019/03/18_
- Fix a minor issue when testing for requested production build.
### __[1.0.1](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.1)__ | _2019/03/18_
- Add failsafe when importing Seafile's APT-key
- Restrict production build to latest, majors, minors and revisions version, on-demand.
# __[1.0.0](https://gitlab.com/flwgns-docker/seafile-client/-/tags/1.0.0)__ | _2019/03/15_
- Release to Docker Hub

### __[0.9.2](https://gitlab.com/flwgns-docker/seafile-client/-/tags/0.9.2)__ | _2019/03/15_
- Test release on GitLab, before Docker Hub
