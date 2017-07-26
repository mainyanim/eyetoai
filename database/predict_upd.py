import pyodbc

config = dict(server = 'tcp:eyetoaidevelopment.database.windows.net',
              port = 1433,
              database = 'test',
              username = 'michael',
              password = 'GradioAI7000')


conn_str = ('SERVER={server},{port};'   +
            'DATABASE={database};'      +
            'UID={username};'           +
            'PWD={password}')

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};' +
    conn_str.format(**config)
    )


cursor = conn.cursor()

def condition_i(c,f):
    """
    rep_num returns number of reports with specific condition
    cond_freq returns condition frequency in all reports
    :param cond: string, condition name
    :return: prior probability of specific condition (?)
    """
    """
    rep_num is an array returning tuples of pairs (condition, number of reports with this condition),
    condtotal is total number of conditions in the reports since one report can contain several conditions
    cond_freq is number of reports where cond_0 appears
    """

    cursor.execute("SELECT  Conditions.Name, COUNT (DISTINCT ReportId) " 
                   "FROM ReportConditionFindingOptions "
                   "INNER JOIN Conditions "
                   "ON ReportConditionFindingOptions.ConditionId = Conditions.Id "
                   "GROUP BY Conditions.Name ")
    rep_num = cursor.fetchall()
    cond_total = [sum(rep_num[x][1] for x in range(len(rep_num)))][0]
    cursor.execute("SELECT COUNT (DISTINCT ReportId) " 
                   "FROM ReportConditionFindingOptions "
                   "INNER JOIN Conditions "
                   "ON ReportConditionFindingOptions.ConditionId = Conditions.Id "
                   "WHERE Name = ? GROUP BY Conditions.Name", c)
    cond_freq = cursor.fetchval()
    pr_cond_0 = cond_freq/cond_total
    print(pr_cond_0)
    cursor.execute(" SELECT COUNT (FindingId) "
                   " FROM ReportConditionFindingOptions "
                   " INNER JOIN Findings "
                   " ON ReportConditionFindingOptions.FindingId = Findings.Id"
                   " WHERE FindingId IN (SELECT Id FROM Findings "
                   " WHERE Name = ? ) AND ConditionId IN (SELECT Id FROM Conditions WHERE Name = ?)"
                   " GROUP BY ReportId", f, c)
    find_0 = cursor.fetchall()
    print(find_0)
    return pr_cond_0


if __name__ == '__main__':
    condition_i('Fibroadenoma', 'Mass')