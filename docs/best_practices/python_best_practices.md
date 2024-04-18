# Best Practices for Python

## Using `venv` to manage dependencies:

Dependency management on the HPC can be very difficult. The `venv` module
allows you to set up a virtual environment that isolates the dependencies for
each individual project by installing them into a project-specific folder. This
is an intergral part of writing reproducible code and is useful for two
reasons:

1. Virtual environments allow you to clearly communicate your code's required dependencies to your collaborators
1. Virtual environments ensures that updating dependencies for one project will never break dependencies for another project (this is an issue when two projects rely on different versions of the same package)

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

You can check out more info about the `venv` module and virtual environments on the [python language website](https://docs.python.org/3/tutorial/venv.html)
