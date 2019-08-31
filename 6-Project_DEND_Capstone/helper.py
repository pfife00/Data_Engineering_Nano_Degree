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
