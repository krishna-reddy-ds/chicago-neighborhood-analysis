import os

STATE = "17"
COUNTY = "031"
API_KEY = os.getenv("CENSUS_API_KEY", "")

CAS = {
    "15": "Portage Park",
    "25": "Austin",
    "53": "West Pullman",
    "62": "West Elsdon"
}

CA_COORDS = {
    "15": (41.9534, -87.7665),
    "25": (41.8986, -87.7479),
    "53": (41.6929, -87.6366),
    "62": (41.7896, -87.7243)
}

ACS2022 = "https://api.census.gov/data/2022/acs/acs5"
ACS2014 = "https://api.census.gov/data/2014/acs/acs5"

VARIABLES = {
    "B01003_001E": "total_pop",
    "B02001_002E": "white_alone",
    "B02001_003E": "black_alone",
    "B03003_003E": "hispanic",
    "B15003_001E": "edu_total",
    "B15003_022E": "ba_degree",
    "B15003_023E": "masters",
    "B15003_024E": "professional",
    "B15003_025E": "doctorate",
    "B25003_001E": "tenure_total",
    "B25003_002E": "owner_occupied",
    "B25003_003E": "renter_occupied",
    "B25002_001E": "housing_units_total",
    "B25002_003E": "vacant_units",
    "B19013_001E": "median_hh_income",
    "B25064_001E": "median_gross_rent",
    "B05002_013E": "foreign_born",
    "B08301_001E": "commute_total",
    "B08301_019E": "walk_to_work",
}

CA_TRACTS = {
    "15": ["800100", "800200", "800300", "800400", "800500", "800600", "800700", "800800"],
    "25": ["250100", "250200", "250300", "250400", "250500", "250600", "250700", "250800"],
    "53": ["530100", "530200", "530300", "530400", "530500"],
    "62": ["620100", "620200", "620300", "620400", "620500", "620600"]
}
