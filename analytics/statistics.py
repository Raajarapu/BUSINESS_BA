def descriptive_statistics(df):
    return df.describe(include="all").to_dict()

def correlation_analysis(df):
    numeric = df.select_dtypes(include="number")
    return numeric.corr().to_dict()
