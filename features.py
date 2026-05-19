import numpy as np
import pandas as pd
from config import VARIABLES

def compute_features(df):
    for var in VARIABLES.keys():
        df[var] = pd.to_numeric(df[var], errors='coerce')

    df = df.replace(-666666666, np.nan)
    df = df.replace(-999999999, np.nan)
    df = df.replace(0, np.nan)

    df['share_white'] = df['B02001_002E'] / df['B01003_001E']
    df['share_black'] = df['B02001_003E'] / df['B01003_001E']
    df['share_hispanic'] = df['B03003_003E'] / df['B01003_001E']

    ba_plus_cols = ['B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E']
    df['ba_plus_total'] = df[ba_plus_cols].sum(axis=1)
    df['share_ba_plus'] = df['ba_plus_total'] / df['B15003_001E']

    df['renter_share'] = df['B25003_003E'] / df['B25003_001E']
    df['homeownership_rate'] = df['B25003_002E'] / df['B25003_001E']
    df['vacancy_rate'] = df['B25002_003E'] / df['B25002_001E']

    df['med_income'] = df['B19013_001E']
    df['med_income_log'] = np.log1p(df['med_income'])
    df['med_rent'] = df['B25064_001E']
    df['med_rent_log'] = np.log1p(df['med_rent'])

    df['foreign_born_share'] = df['B05002_013E'] / df['B01003_001E']
    df['walk_to_work_share'] = df['B08301_019E'] / df['B08301_001E']

    return df

def create_temporal_analysis(df_2014, df_2022):
    metrics = ['med_income', 'share_ba_plus', 'foreign_born_share',
               'homeownership_rate', 'vacancy_rate']

    comparison = {}

    for metric in metrics:
        try:
            if metric in df_2014.columns and metric in df_2022.columns:
                val_2014 = df_2014[metric].median()
                val_2022 = df_2022[metric].median()

                if pd.notna(val_2014) and pd.notna(val_2022) and val_2014 > 0:
                    pct_change = ((val_2022 - val_2014) / val_2014) * 100
                    comparison[metric] = {
                        '2014': val_2014,
                        '2022': val_2022,
                        'change_pct': pct_change
                    }
        except Exception:
            continue

    return comparison
