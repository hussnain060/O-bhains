class Config:

    """
    This module stores all the configuration variables

    Parameters
    ----------
    pull_data_from_date : str, yyyy-mm-dd
        To pull historical data from a specific date, by default 2020-01-01
    
    average_by : str
        Summarize data by taking the average, by default 'hour'
        available options: 'month','week','day','hour','minuts','none'
    
    average_criteria:str
        choose mean or medain as average calculation method , by default median

    """

    def __init__(self):

        # configure data pull option
        self.pull_data_from_date: str = "2021-01-01"

        # configure summary options
        self.average_by: str = "hour"
        self.average_criteria: str = "median"

