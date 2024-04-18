library(duckplyr)
library(tidyverse)

data_set <- '/gpfs/milgram/pi/medicaid_lab/data/cms/ingested/unpartitioned_compressed/taf_demog_elig_base/*/*'

df <- duckplyr_df_from_parquet(data_set) %>%
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
  
