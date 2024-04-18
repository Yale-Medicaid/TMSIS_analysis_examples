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
