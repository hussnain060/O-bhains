class Config:

    """
    This module stores all the configuration variables

    Parameters
    ----------
    pull_data_from_date : str, yyyy-mm-dd
        To pull historical data from a specific date, by default 2020-01-01
    
    average_by : str
        Summarize data by taking the average, by default 'day'
        available options: 'month','week','day','hour','minuts','none'

    """

    # configure data pull option
    pull_data_from_date: str = "2021-01-01"

    # configure summary options
    average_by: str = "day"

