
Base images
===========

How to make updates:

1. Create a new branch
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
    1. Do whatever node/yarn things you people do ;-)
1. Bump the version in [VERSION file](VERSION)
1. Commit your changes
1. Open a pull request; if necessary
1. Commit and tag it `make tag`
1. Merge it to master
1. Delete the branch
1. Push
1. Update child projects to use this new version
