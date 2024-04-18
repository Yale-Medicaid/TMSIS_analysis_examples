# Example Summaries

## Reproducing Eligibility Statistics

[R code example](R_examples/example_1.md) | [Python code example](R_examples/example_1.md)

This example involves repdocucing [medicare eligibility statistics](https://www.medicaid.gov/dq-atlas/landing/topics/single/table?topic=g3m13&tafVersionId=23) DQATLAS. It's an ideal point of entry for researchers wanting to run simple queries on the TMSIS data using either R or Python, and will teach you the basics of working with the HPC cluster. Specifically, the example includes code to:

1. Load the SLURM modules needed for the task (python, R, etc)
1. Register the datasets with R / Python without loading them into memory.
1. Run compute against these datasets and report the results.

