# Best Practices for R

## Using `renv` to manage dependencies:

Dependency management on the HPC can be very difficult. `renv` allows you to
set up a virtual environment in R that isolates the dependencies for each
individual project. This is useful for two reasons:

1. It allows you to clearly communicate your code's required dependencies to your collaborators
2. Updating dependencies for one project will never break dependencies for another project

Virtual environments have already been set up for all of the example projects, and the virtual environment will be activated whenever you open a new R session in these directories (so if you start your project by copying one of these directories, you are good to go).
To set up `renv ` on a new project, simply call `renv::init()` in R while in the project home folder. You can then use either `renv::install()` or `install.packages()` to install packages as normal.

More info about getting started with `renv` can be found [here](https://rstudio.github.io/renv/articles/renv.html).

## Using `duckplyr` to conduct large-scale data analysis.

Another important skill is using a query engine like
[DuckDB](https://duckdb.org/) to run queries on datasets without loading them
into memory.

If you don't work with large-scale data, you are probably most familiar with a
workflow that looks something like this:

1. Read the data into R using `read_csv` or an alternative
1. Run models and analysis on the data using dplyr
1. Save out the results to another file

When datasets get large, this workflow begins to break down as it becomes very
slow (if not impossible) to load the data into memory in order to analyze. This
is where technologies like DuckDB can help - you can register data with DuckDB
without reading it into memory, and then write queries that access and load
only the relevant parts of your data for analysis, saving time and resources.

Importantly, new packages like `duckplyr` provide you a way to do this while
still using dplyr-syntax. The first example, `eligibility_example/` is a great
example of this: using duckplyr allows us to compute summary statistics on a
massive dataset, *using dplyr-syntax,*  without reading the entire dataset into
memory.

To learn more about `duckplyr` check out these resources:

* [This post announcing duckplyr on duckdb.org](https://duckdb.org/2024/04/02/duckplyr.html)
* [This presentation by Kirill Müller at `posit::conf`](https://www.youtube.com/watch?v=V9GwSPjKMKw) introducing duckplyr and demonstrating some of its' features
* [This talk by Hannes Mühleisen at `posit::conf`](https://www.youtube.com/watch?v=9OFzOvV-to4) talking about DuckDB, the query engine / database that backs up duckplyr


