# TMSIS Data Documentation

This website provides documentation for our TMSIS datasets for researchers within / collaborating with the Yale Medicaid Lab. On the site, you can find resources explaining the structure of the datasets, recommendations for working with large datasets, and example code from other projects that have used the same data.

## Hive-Partitioned Datasets:

CMS gives us the data in a bespoke fixed-width file format called `.fts`. Working with these files is generally slow (as the file format is not optimized for database queries), and cumbersome (as one must implement their own parsing logic to read the files). We parse and format the TMSIS data into a series of [hive partitioned](https://duckdb.org/docs/data/partitioning/hive_partitioning.html) [parquet files](https://parquet.apache.org/), a standardized file format that is fast to read, supports modern database operations, and enforces strong types, so you never have to worry that your files have been read in incorrectly.

To get started, with the files, you can log into Milgram and open the directory where they are stored on the server. The files are currently located at `/gpfs/milgram/pi/medicaid_lab/data/cms/ingested/TMSIS_TAF`.

```sh
cd /gpfs/milgram/pi/medicaid_lab/data/cms/ingested/TMSIS_TAF
```

Opening this directory, you will see the following sub-directories:

```
TMSIS_taf/
├── taf_demog_elig_base
├── taf_demog_elig_dates
├── taf_demog_elig_disability
├── taf_demog_elig_hh_spo
├── taf_demog_elig_mngd_care
├── taf_demog_elig_mny_flw_prsn
├── taf_demog_elig_waiver
├── taf_inpatient_header
├── taf_inpatient_line
├── taf_inpatient_occurrence
├── taf_long_term_header
├── taf_long_term_line
├── taf_long_term_occurrence
├── taf_other_services_header
├── taf_other_services_line
├── taf_other_services_occurrence
├── taf_rx_header
└── taf_rx_line
```

The directories fall into 5 groups, the pharmacy files (taf_rx_.\*), the
long-term care files (taf_long_term_.\*), the inpatient files
(taf_inpatient_.\*), the other care files (taf_other_services_.\*) and the demographic and eligibility files
(taf_demog_elig_.\*). You can find quick links to the ResDAC documentation for each
file type at the bottom of this page.

If we open the `taf_demog_elig_base` directory, we can see that the data is
further partitioned at the state-year level. If you are performing data
analysis on a state in a single year, you can simply take one of these files
and start performing data analysis on it. Alternatively, if you are more
familiar with `arrow` and `DuckDB`, you can use this file structure to speed up
queries that are run on specific states or years. Check out the [R
examples](examples/R_examples/example_1/) for more information on how to do
this if you are curious.

```
taf_demog_elig_base/
├── year=2016
│   ├── state=AK
│   │   └── data.paquet
│   ├── state=AL
│   │   └── data.paquet
│   └── ...
├── year=2017
│   ├── state=AK
│   │   └── data.paquet
│   ├── state=AL
│   │   └── data.paquet
│   └── ...
└── ...
```

## ResDAC Documentation Links:

ResDAC provides extensive documentation for all of the files we use. No column
names or datatypes have been changed in formatting the dataset into `parquet`
format, so all the documentation presented on this website applies to the
standardized files as well as the raw files.

* [Documentation for other services files](https://resdac.org/cms-data/files/taf-ot)
* [Documentation for demographic and eligibility files](https://resdac.org/cms-data/files/taf-de)
* [Documentation for inpatient files](https://resdac.org/cms-data/files/taf-ip)
* [Documentation for long term care files](https://resdac.org/cms-data/files/taf-lt)
* [Documentation for pharmacy files](https://resdac.org/cms-data/files/taf-rx)

