def descriptive_statistics(df):
    """
    Returns descriptive statistics for all columns
    """
    return df.describe(include="all").to_dict()


def correlation_analysis(df):
    """
    Returns correlation matrix for numeric columns
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return {}
    return numeric_df.corr().to_dict()
