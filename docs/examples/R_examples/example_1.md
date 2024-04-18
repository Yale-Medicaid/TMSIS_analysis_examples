# Example 1 - Reproducing Eligibility Statistics

This example involves reproducing [these eligibility statistics]( https://www.medicaid.gov/dq-atlas/landing/topics/single/table?topic=g3m13&tafVersionId=23) from DQATLAS, which give the number of enrollees in one of three age groups in 2019. Source code for this example can be found [here](https://github.com/Yale-Medicaid/TMSIS_data_documentation/tree/main/R/eligibility_example).

This task is a good point of introduction for users wanting to learn how to use
[Arrow](https://arrow.apache.org/) and [DuckDB](https://duckdb.org/) to
expeditiously run queries on large datasets, and for researchers wanting to
learn the SLURM workflow.

## Step 1: Writing the R Code

The first step is to write the R code needed to execute our query. We first
register the eligibility dataset that we will be using with R using
`duckplyr_df_from_parquet()`, which registers the datasets with R without
reading them into memory.  This is important because the dataset would take a
long time to load into R, and because we are only interested in a subset of the
data (the age, state, year, and recipient ID columns).

We then run some simple dplyr code to filter to the rows we are interested in
(observations in 2019), and select only the appropriate columns. Importantly,
while this code is written in expressive `dplyr` syntax, it's actually run
using DuckDB, so it executes crazy-fast. The final steps summarize the number
of observations in each age group, and transform the outcome into a layout
closer to the one on the DQATLAS website.


```r title="example.R"
library(duckplyr)
library(tidyverse)

data_set <- '/gpfs/milgram/pi/medicaid_lab/data/cms/ingested/unpartitioned_compressed/taf_demog_elig_base/*/*'

df <- duckplyr_df_from_parquet(data_set) %>% # Registers dataset with R
  # Remove "dummy" records for members that only appear in claims data and never have an eligibility record
  filter(MISG_ELGBLTY_DATA_IND == 0, year == 2019L) %>%
  select(MSIS_ID, AGE_GRP_CD, STATE_CD) %>%
  # Documentation uses AGE_GRP_CD, but note some people have AGE = -1 but AGE_GRP_CD = 1...
  # 0-18 = AGE_GRP_CD in [1,2,3,4]
  # 19-64 = AGE_GRP_CD in [5,6,7]
  # 65+ = AGE_GRP_CD in [8,9,10]
  mutate(age_group =
           case_when(
             AGE_GRP_CD %in% c(1,2,3,4) ~ "0-18",
             AGE_GRP_CD %in% c(5,6,7) ~ "19-64",
             AGE_GRP_CD %in% c(8,9,10) ~ "65+",
             TRUE ~ "Missing"
                     )
           ) %>%
  summarize(
    n = n_distinct(MSIS_ID),
    .by = c(STATE_CD, age_group)
            )

df <- df %>%
  # "Widen" dataframe by making each age-group total a column
  pivot_wider(id_cols = STATE_CD, names_from=age_group, values_from = n) %>%
  mutate(Missing = replace_na(Missing,0)) %>%
  mutate(N = `19-64` + `0-18` + `65+` + Missing) %>%
  arrange(STATE_CD)

print(df, n=100)

```

## Step 2: Writing the SLURM Script

To run analysis code on the cluster, you must submit a job to
[SLURM](https://slurm.schedmd.com/overview.html), the workload manager
responsible for provisioning computer resources for users and running jobs that
are submitted to it. This section shows how to write a SLURM job script to get
the R code we have written running on the cluster.

SLURM job scripts are essentially bash scripts with a special header which
dictates the paramaters used to run the code. When the job is submitted, SLURM
will wait for the necessary resources to become available and then run the bash
script with the parameters you provide. A script we use to run our R code can
be found below. To send this script to slurm, you can run `sbatch submit.sh` in
the terminal.

```sh title="submit.sh"
#!/usr/bin/bash
#SBATCH --job-name=TMSIS_example_analysis
#SBATCH --time=00:20:00
#SBATCH --mail-type=all
#SBATCH --partition=day
#SBATCH --mem=40GB
#SBATCH --cpus-per-task=5
#SBATCH --output=out.txt
#SBATCH -e err.txt

module add R/4.3.0-foss-2020b # Load R

Rscript example.R # Run the R script
```

Parameters passed to slurm are fed in using lines that start with `#SBATCH --{parameter_name}`. The most important parameters are the following:

* `--partition` which dictates which partition the job runs on. This is important to consider because different partitions have different resources available, so you may need to change your partition to run large jobs.
* `--mem` which dictates the memory available to the analysis job. If you specify this too low, your job may run out of memory and crash. Setting this too high means that you may wait a long time for the requested resources to become available.
* `--time` The maximum time allowed for the job to be run before it is terminated by SLURM. Again, there is a balancing act here between selecting enough time for your job to complete, without setting it so high that it is difficult for the job to be scheduled.

You can read more about these parameters at either the [SLURM website](https://slurm.schedmd.com/overview.html) or the [Yale HPC website](https://docs.ycrc.yale.edu/clusters/milgram/), which has specific info about what options are available on Milgram.


