# Using The Data Ingestion Pipeline

We have constructed a code pipeline which takes data in the format provided by
CMS and processes it into a set of standarized, high-performace `.parquet`
files suitable for large-scale data analysis. This guide is intended for
readers interested in learning more about the pipeline and those looking to
importing new years of data.

## How Does the Pipeline Work?

At a very high level, the pipeline completes the following steps that are needed to transform the files from the format given by CMS to a format suitable for speedy analysis:

1. Scan listed 'import' directories for files in the format given by CMS (`.fts` files with associated `.dat` headers). Create a listing of these files.
2. Associate `.fts` files with their `.dta` header files, which provide the metadata necessary to parse them. Read the metadata files to create schemas for each file that is read in.
3. Convert `.fts` files into `.parquet` files, which are faster and have a standardized schema that ensures data types are the same between files of the same type.
4. [Partition](https://duckdb.org/docs/data/partitioning/hive_partitioning.html) the `.parquet` files, which speeds up queries run on specific states / years.

These steps are administered by a build system called [Targets](https://books.ropensci.org/targets/) which keeps track of which steps have been run on each file provided by CMS, and will re-ingest files if they are changed, or if we make a change to the code responsible for processing them. Targets also watches for new data files, and ingests them when run. It automatically keeps track of files that have already been processed, and won't re-ingest an old file if nothing about it has changed. You can ask targets to run the pipeline in response to any changes using the `targets::tar_make()` command in R from inside the pipeline root directory. We also provide a `submit.sh` script that can be run using `sbatch` provisions the neccessary resources for the pipeline using SLURM, and sets it running.

## Adding New Datasets

We have tried to construct the pipeline with extenisibility in mind, and have
taken steps to ensure that you can easily add new regions or types of data from
CMS. To add new data, you should extract the data to a directory that is
accessible by the pipeline and list this directory in the `input_directories`
list in the `_targets.R` file. The relevant lines are highlighted below:

```r title="_targets.R" linenums="1" hl_lines="20 21 22 23 24"
library(targets)
library(arrow)
library(crew)

source('R/ingestion.R')
source('R/hive_partition.R')

tar_option_set(
  packages = c("arrow", "tidyverse", "stringr", "duckplyr"),
  controller = crew_controller_local(workers = 20,
				     local_log_directory="job_outputs/",
				     local_log_join = TRUE,
				     seconds_launch=90,
				     seconds_interval=3)
)

options(readr.num_threads=1)
set_cpu_count(1)

input_directories <-list( # (1)
  "/gpfs/milgram/pi/medicaid_lab/data/cms/raw/dua57871-ndumele/2018/",
  "/gpfs/milgram/pi/medicaid_lab/data/cms/raw/dua57871-ndumele/2017/",
  "/gpfs/milgram/pi/medicaid_lab/data/cms/raw/dua59119-busch/"
)

```

1.  This list gives the locations the pipeline should look for new files to
    ingest. To add a new data extact from TMSIS, unzip it into a directory,
    then list that directory here.

The source code for the ingestion pipeline can be found [here](https://github.com/Yale-Medicaid/TMSIS_ingestion).

