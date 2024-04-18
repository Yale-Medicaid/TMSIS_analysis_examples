# Best Practices for Python

## Using `venv` to manage dependencies:

Dependency management on the HPC can be very difficult. The `venv` module
allows you to set up a virtual environment in R that isolates the dependencies
for each individual project by installing them into a project-specific folder.
This is useful for two reasons:

1. It allows you to clearly communicate your code's required dependencies to your collaborators
1. Updating dependencies for one project will never break dependencies for another project

To create a new virtual environment for your python, you can run the following command:

```sh
python -m venv {path_to_virtual_environment}
```

which creates a new virtual environment at the specified location. In the
example repositories, the virtual environment is located in `./venv/`.

To have the virtual environment manage your dependencies, you have to
`activate` it, which is done with the following command:

```sh
source {path_to_virtual_environment}/bin/activate
```

While the virtual environment is activated, you can use pip as you normally
would, but all changes you make by installing packages will be isolated to this
project. When you are done using the virtual environment, you can either press
`Ctrl+d` (if working interactively), or use the `deactivate` command which will
return your shell to normal. To get a snapshot of the packages used in the venv
(say, to generate a `requirements.txt` file), you can run `pip freeze`.
