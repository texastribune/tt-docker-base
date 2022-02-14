tt-docker-base
===========

This project contains the base Docker image of dependencies for the Texas Tribune website and CMS. It serves as the starting point for a [multistage docker build](https://docs.docker.com/develop/develop-images/multistage-build/).

## Testing Dependabot PRs

Github's dependabot regularly creates PRs that bump package versions in order to fix known security issues. To ensure that these updates don't cause unexpected behavior on the Texas Tribune website, we prefer to test them locally before merging and deploying them.

Consult our [dependabot testing guide](https://texastribune.atlassian.net/wiki/spaces/TECH/pages/1992163329/How+to+deploy+dependabot+fixes) for step-by-step instructions on testing and deploying.

## Updating dependencies

The following instructions provide a general guide to updating, adding or removing Python and Node dependencies in this repo.

### Setup
```sh
# bring down latest
git pull origin master

# create a feature branch for your changes
git checkout -b <new-branch-name>
```
### Add or Update Dependencies
#### Python Dependencies
If you're adding or updating a python dependency:
   1. Run a shell inside a container
      ```sh
         make base-shell
      ```
   1. Add or update python dependency
      ```sh
      # from inside the container shell from step 1:

      # add a new production python dependency
      poetry add <package>

      # add a new development dependency
      poetry add --dev <package>

      # pin the dependency to a specific version like this
      poetry add <package>@1.0.0

      # example for updating an existing package to 1.0.1
      poetry update packagename@1.0.1
      ```
   1. Return to your local machine's shell
      ```sh
      exit
      ```
   1. Proceed to [build and test locally](#build-and-test-new-images-locally).
Though recommended to use the poetry CLI, another way to accomplish the same is to edit `pyproject.toml` manually, then run `poetry lock` in the shell inside the container.

See the [poetry docs](https://poetry.eustace.io/docs/) for more commands and details on usage.

#### Node Dependencies
If you're adding or updating a node dependency:
   1. Run a shell inside a container
      ```sh
      make dev-shell
      ```
   1. Add or update node dependency
      ```sh
      # from inside the container shell from step 1:

      # enter the node directory
      cd node

      # add a new package
      npm install --save <package-name> # use --save-dev if dev dependency

      # add a specific version of a package
      npm install --save <package>@1.0.0

      # get help on npm for further usage
      npm help
      ```
   1. Return to your local machine's shell
      ```sh
      exit
      ```
   1. Proceed to [build and test locally](#build-and-test-new-images-locally).
### Build and Test New Images Locally
1. Build new images locally based on your python or node dependency updates
   ```sh
   # from your local machine's shell - not the container!

   make images
   ```
   This creates two local images:
     - `texastribune/base:<git-branch-name>-dev`
     - `texastribune/base:<git-branch-name>-base`

   You can check that they were successfully created by runnning:
      ```sh
      docker images | $(git branch --show-current)

      # example output:
      texastribune/base          branchname-dev          2707ec0fcf6b        22 minutes ago      2.24GB
      texastribune/base          branchname-base         8a387eac996c        59 minutes ago      1.37GB

      ```

1. Test it locally
   - Switch to your local `texastribune` repo:
     - Update the `BASE_PRODUCTION_VERSION` and `BASE_DEVELOPMENT_VERSION` variables
      - See `texastribune` docs for they should be updated, or use your text editor search.
   -  Create a `texastribune` PR.
1. If all looks good, proceed to [deploy steps](#deploy).

### Deploy
#### Build the New Base Images
If this is a small change that's very unlikely to affect anyone else, you'll build your [new images directly through `master`](#directly-to-master-branch), otherwise [build your images through your feature branch](#through-tt-base-feature-branch).
##### Directly to Master Branch
1. Commit your changes to your `tt-base` branch.
1. Merge this branch into `master` and proceed to [steps to deploy texastribune](#deploy-texastribune).
1. Immediately bump the version in the [VERSION file](VERSION), commit and tag: `make tag`. There should be as little gap as possible between this step and the previous one so as to avoid conflicts with other committers. You don't need to push anything. The `make tag` command will push it for you.
1. Proceed to [deploy to texastribune steps](#deploy-texastribune).

##### Through tt-base Feature Branch
1. Commit your changes to your `tt-base` branch.
1. Push your branch.
    - Docker Hub will build the images with the same name as when you [built them locally](#build-and-test-new-images-locally).
    - Now anyone can pull down and use the images `texastribune/base:<git-branch-name>`
    - Update your associated `texastribune` PR to use these ^ images built from the `tt-base` feature branch.  Anyone can pull that PR's branch down to test locally.
    - You can check the status of the builds on [Docker Hub](https://hub.docker.com/repository/docker/texastribune/base). _You'll see a more accurate build log when logged-in under an account that is affiliated with the texastribune org in Docker Hub._
1. After the related `texastribune` PR is approved, merge your `tt-base` feature branch into master, and delete the feature branch.
1. `git checkout master` and `git pull` to get your local master branch even with remote.
1. Immediately bump the version in the [VERSION file](VERSION), commit and tag: `make tag`. There should be as little gap as possible between this step and the previous one so as to avoid conflicts with other committers. You don't need to push anything. The `make tag` command will push it for you.
1. Proceed to [deploy to texastribune steps](#deploy-texastribune).

#### Deploy texastribune
1. Change your related `texastribune` PR to use the tag instead of the branch name (example: `texastribune/base:1.2.14-base` and `texastribune/base:1.2.14-dev`). See the `texastribune` README for the locations to change the version. You may want to wait until the Docker Hub build is complete before pushing your `texastribune` PR image version because the CI tests will fail if the image isn't available yet.
1. **Make sure [Docker Hub](https://hub.docker.com/repository/docker/texastribune/base) has built the image with the tag before deploying the `texastribune` PR**. In an emergency you can leave in the branch name -- the image should
   already be built by Docker Hub and it won't go away even when the branch is deleted.
1. Merge related `texastribune` PR.
1. Deploy it
1. Your work is done.
