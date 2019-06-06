
Base images
===========

How to make updates:

1. `git pull origin master`. Do not create a new branch or PR. To minimize conflicts it works best if you can complete all the steps below together without gaps.
1. If you're adding a python dependency:
    1.  Run `make run-base`
    1. Run `poetry add --dev <package>` (drop the `--dev` if it's a production
       dependency) 
    1. For other operations see the
       [poetry docs](https://poetry.eustace.io/docs/)
    1. Maybe edit `pyproject.toml` by hand if necessary
    1. Run `poetry lock`
1. If it's a node dependency:
    1. Run `make run-dev` 
    1. `yarn add <dependency name>`
    1. Or do whatever node/yarn things you people do ;-)
1. If you modify either `Dockerfile.base` or `Dockerfile.dev`:
    1. run `make prepare` after
1. Bump the version in [VERSION file](VERSION)
1. Commit and push your changes to master.
1. Tag and push a new tag with `make tag`.
1. If you're merging Dependabot PRs:
    1. merge the PR (maybe merge multiple ones to batch them)
    1. `git checkout master; git merge dependencies`
    1. Bump the version in [VERSION file](VERSION)
    1. Commit and tag it `make tag`
1. Update child projects to use this new version
