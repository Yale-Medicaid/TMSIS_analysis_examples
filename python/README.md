# TMSIS Analysis Examples

Beniamino Green (<beniamino.green@tuta.com>) (<beniamino.green@yale.edu>) and Anthony Lollo
(<anthony.lollo@yale.edu>)

# Introduction:

This analysis houses example code and Documentaiton to help researchers get
started using our TMSIS datasets.

# Examples:

## Example 1 - Reproducing Eligibility Statistics

This example involves reproducing [these eligibility statistics](
https://www.medicaid.gov/dq-atlas/landing/topics/single/table?topic=g3m13&tafVersionId=23) from medicaid.gov. It's a good point of introduction for users wanting to learn how to use [Arrow](https://arrow.apache.org/) and [DuckDB](https://duckdb.org/) to expeditiously run queries on large datasets, and for researchers wanting to learn the SLURM workflow.

Jobs are exectued by running `submit.sh` in the `R/` and `python/` example folders respectively. These scripts submit jobs to the workload manager, [SLURM](https://slurm.schedmd.com/overview.html), which is responsible for starting jobs when the resources needed to run them become available.

Each job invloves running the following steps:

1) Loading the SLURM modules needed for the task (python, R, etc)
2) Sourcing the virtual environment for the project (loading required packages for each piece of software)
3) Registering the datasets with R / Python without loading them into memory.
4) Running compute against these datasets and reporting the results.

