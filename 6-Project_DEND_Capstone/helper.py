import re

def clean_temp_data(df):
    """
    Clean temperature data by removing missing temperature data and removing duplicate entries
    """

    #filter out missing average temperature values
    df = df.filter(df.AverageTemperature != 'NaN')

    #remove duplicate entries
    df = df.dropDuplicates(['City', 'Country'])

    #drop uncessary columns
    df = df.drop('AverageTemperatureUncertainty')

    return df


def clean_i94_data(df, i94port_valid):
    """
    Clean immigration data by filtering out NaN and dropping unecssary columns
    """

    # Filter where i94port is null
    df = df.filter(df.i94port.isin(list(i94port_valid.keys())))

    #drop unecessary columns
    df = df.drop('occup', 'entdepu', 'insnum')

    return df

def check_pop_data(df):
    """
    check demographics data for invalid population entries
    """
    i=0
    for index, row in df.iterrows():
        #if sum of males and females is greater than total population, then there is an issue with the data
        if(row['Male Population'] + row['Female Population'] != row['Total Population']):
           print("Issue with number of males or females are row: ", row)
           print(i)

            #if number of veterans or the number of foreign-born people are greater than total population, then there is an issue with the data
        elif(row['Number of Veterans'] > row['Total Population'] or row['Foreign-born'] > row['Total Population']):
           print("Issue with number of foreign born or number of veterans at row: ", row)
           print(i)
        i+=1

def clean_demo_data(df):
    """
    remove unecesary columns from data
    """
    #specify columns to drop (gender columns)
    drop_cols = ['Male Population', 'Female Population']

    #drop those values in the Male Population and Female Population columns which contain NaNs
    df = df.dropna(subset=drop_cols)

    #use pandas to rename method to rename State Code to State_Code
    df.rename(columns={'State Code':'State_Code'}, inplace=True)

    return df

def quality_check(df, description):
    """
    Take dataframe as input and print out result of data quality check.
    """
    result = 0
    result = df.count()
    if result == 0:
        print("Data quality check failed for {} with zero records".format(description))
    else:
        print("Data quality check passed for {} with {} records".format(description, result))


def get_i94port_valid(file):
    """
    Create valid i94port dictionary from input text file for creating fact table
    """
    re_obj = re.compile(r'\'(.*)\'.*\'(.*)\'')
    i94port_valid = {}
    with open(file) as f:
        for line in f:
            match = re_obj.search(line)
            i94port_valid[match[1]]=[match[2]]
    return i94port_valid
