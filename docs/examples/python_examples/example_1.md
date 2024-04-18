# Example 1 - Reproducing Eligibility Statistics

This example involves reproducing [these eligibility statistics]( https://www.medicaid.gov/dq-atlas/landing/topics/single/table?topic=g3m13&tafVersionId=23) from DQATLAS, which give the number of enrollees in one of three age groups in 2019. Source code for this example can be found [here](https://github.com/Yale-Medicaid/TMSIS_data_documentation/tree/main/python/eligibility_example).

This task is a good point of introduction for users wanting to learn how to use
[Arrow](https://arrow.apache.org/)  and
[pyarrow](https://pypi.org/project/pyarrow/) and for researchers wanting to
learn how to submit jobs on the HPC.

## Step 1: Python Code

```r title="example.py"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pyarrow.parquet as pq
import pyarrow.compute as pc

data_set = '/gpfs/milgram/pi/medicaid_lab/data/cms/ingested/dua57871-ndumele/2017/taf_demog_elig_base_res000019152_req011826/'

states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
        "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN",
        "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH",
        "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA",
        "WI", "WV", "WY"]

abbrev_to_name = { "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ":
        "Arizona", "CA": "California", "CO": "Colorado", "CT": "Connecticut",
        "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
        "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "KS":
        "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts",
        "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
        "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina",
        "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire",
        "NJ": "New Jersey", "NM": "New Mexico", "NV": "Nevada", "NY": "New York",
        "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
        "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
        "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia",
        "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin",
        "WV": "West Virginia", "WY": "Wyoming"}

cols = ['BENE_ID', 'STATE_CD', 'AGE', 'AGE_GRP_CD', 'MISG_ELGBLTY_DATA_IND', 'MSIS_ID']
table = pq.read_table(data_set, columns=cols)
print(table.nbytes/10**9)

d = {}
for state in states:
    df = table.filter(pc.equal(table['STATE_CD'], state)).to_pandas()
    # Remove "dummy" records for members that only appear in claims data and never have an eligibility record
    df = df[df['MISG_ELGBLTY_DATA_IND'].eq(0)]

    # Documentation uses AGE_GRP_CD, but note some people have AGE = -1 but AGE_GRP_CD = 1...
    # 0-18 = AGE_GRP_CD in [1,2,3,4]
    # 19-64 = AGE_GRP_CD in [5,6,7]
    # 65+ = AGE_GRP_CD in [8,9,10]
    s = (pd.cut(pd.to_numeric(df['AGE_GRP_CD'], errors='coerce'), [0, 5, 8, np.inf], labels=['0-18', '19-64', '65+'], right=False)
                       .value_counts(normalize=True).mul(100).round(1)
                               )

        # Seems reports use MSIS_ID, though BENE_ID is the better identifier for a member over time...
    s['total'] = df.MSIS_ID.nunique()
    s['missing'] = np.round(df.AGE_GRP_CD.isnull().mean()*100, 1)
    d[abbrev_to_name.get(state)] = s

# Join together all states.
res = (pd.DataFrame.from_dict(d, orient='index').sort_index()
                 .reindex(['total', 'missing', '0-18', '19-64', '65+'], axis=1)
                       )
res['total'] = res['total'].apply(lambda x: f'{x:,.0f}')
res
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
#SBATCH --job-name=TMSIS_python_example
#SBATCH --time=00:20:00
#SBATCH --mail-type=all
#SBATCH --partition=day
#SBATCH --mem=40GB
#SBATCH --cpus-per-task=5
#SBATCH --output=out.txt
#SBATCH -e err.txt

# Load Python
module load Python/3.10.8-GCCcore-12.2.0

# load the virtual environment used for this project
source venv/bin/activate

python example.py
```

Parameters passed to slurm are fed in using lines that start with `#SBATCH --{parameter_name}`. The most important parameters are the following:

* `--partition` which dictates which partition the job runs on. This is important to consider because different partitions have different resources available, so you may need to change your partition to run large jobs.
* `--mem` which dictates the memory available to the analysis job. If you specify this too low, your job may run out of memory and crash. Setting this too high means that you may wait a long time for the requested resources to become available.
* `--time` The maximum time allowed for the job to be run before it is terminated by SLURM. Again, there is a balancing act here between selecting enough time for your job to complete, without setting it so high that it is difficult for the job to be scheduled.

You can read more about these parameters at either the [SLURM website](https://slurm.schedmd.com/overview.html) or the [Yale HPC website](https://docs.ycrc.yale.edu/clusters/milgram/), which has specific info about what options are available on Milgram.


