# How to contribute

This project uses [nbdev](https://nbdev.fast.ai/getting_started.html) for development. Before beginning, make sure that nbdev and a jupyter-compatible client such as jupyterlab or nbclassic are installed. To make changes, update the notebooks in the `nbs` folder, not the .py files directly. Then, run `nbdev_export`. For more details, have a look at the [nbdev tutorial](https://nbdev.fast.ai/tutorials/tutorial.html).

## How to get started

Before anything else, please install the git hooks that run automatic scripts during each commit and merge to strip the notebooks of superfluous metadata (and avoid merge conflicts). After cloning the repository, run the following command inside it:

```sh
nbdev_install_hooks
```

This is a one-off command that you only have to run when you're first setting up the repo locally.

You will also want to set up a `prep` alias in `~/.zshrc` or other shell startup file:

```sh
# nbdev alias to clean Jupyter notebooks before committing
alias prep='nbdev_export && nbdev_clean && nbdev_trust'
```

Run `prep` before each commit.

## Did you find a bug?

* Ensure the bug was not already reported by searching on GitHub under Issues.
* If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
* Be sure to add the complete error messages.

### Did you write a patch that fixes a bug?

* Open a new GitHub pull request with the patch.
* Ensure that your PR includes a test that fails without your patch, and pass with it.
* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

## PR submission guidelines

* Keep each PR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needed to keep each PR focused.
* Do not mix style changes/fixes with "functional" changes. It's very difficult to review such PRs and will most likely get rejected.
* Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
* Do not turn an already-submitted PR into your development playground. If after you submit a PR, you discover that more work is needed: close the PR, do the required work, and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
* If, however, you submit a PR and receive a request for changes, you should proceed with commits inside that PR, so that the maintainer can see the incremental fixes and won't need to review the whole PR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the PR, do the work, and then submit it again. Use common sense where you'd choose one way over another.

## Do you want to contribute to the documentation?

* Docs are automatically created from the notebooks in the nbs folder.
