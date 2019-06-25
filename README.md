
Base images
===========

How to make updates:

1. `git pull origin master`. 
1. Create a new branch.
1. If you're adding a python dependency:
    1. Run `make base-shell`
    1. Run `poetry add --dev <package>` (drop the `--dev` if it's a production
       dependency) 
    1. For other operations see the
       [poetry docs](https://poetry.eustace.io/docs/)
    1. Maybe edit `pyproject.toml` by hand if necessary
    1. Run `poetry lock`
1. If it's a node dependency:
    1. Run `make dev-shell` 
    1. `yarn add <dependency name>`
    1. Or do whatever node/yarn things you people do ;-)
1. Run `make images`. This will create and tag 
   images locally based on the name of the git branch. So if your branch is `upgrade-drf`
   the Docker image names will be `texastribune/base:upgrade-drf-dev` and `texastribune/base:upgrade-drf-base`. You don't need to wait
   for Docker Hub to build the image to test with it locally. You can update
   `BASE_PRODUCTION_VERSION` and `BASE_DEVELOPMENT_VERSION` on your `texastribune`
   PR to `upgrade-drf-base` and `upgrade-drf-dev` respectively.
1. Commit your changes to that branch.
1. If this is a small change that's very unlikely to affect anyone else then merge this
   branch into `master` and skip the next step and any remaining step involving a PR.
1. Push your branch. Docker Hub will build the image with the same names as the previous
   step. Now anyone else can review that PR once the image tagged with the branch name has been built. You can check the status of the builds on [Docker Hub](https://cloud.docker.com/u/texastribune/repository/docker/texastribune/base/general).
1. After the related `texastribune` PR is complete and approved merge this branch to
   master. Delete the branch.
1. Immediately bump the version in the [VERSION file](VERSION), commit and tag: `make tag`. There
   should be as little gap as possible between this step and the previous one so as to
   avoid conflicts with other committers. You don't need to push anything. The `make tag` command will 
   push it for you.
1. Change your related `texastribune` PR to use the tag instead of the branch name. See
   the `texastribune` README for the locations to change the version. You may want to wait until the Docker Hub build is complete before pushing your `texastribune` PR image version because the CI tests will fail if the image isn't available yet.
1. **Make sure Docker Hub has built the image with the tag before deploying the
   `texastribune` PR**. In an emergency you can leave in the branch name -- the image should
   already be built by Docker Hub and it won't go away even when the branch is deleted.
1. Merge and deploy the related `texastribune` PR.
1. Your work is done.
1. If you're merging Dependabot PRs:
    1. merge the PR (maybe merge multiple ones to batch them) - these will be merged to
       the `dependencies` branch; not master
    1. Create your own branch off `master` and merge `dependencies` into it: `git
       checkout -b my-fancy-branch; git merge dependencies`
    1. Resume with the step "Run `make images`..." above. 
