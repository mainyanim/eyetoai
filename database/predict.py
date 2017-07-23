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

def c_i(c, f):
    cursor.execute("SELECT DISTINCT ReportId, COUNT ( DISTINCT ConditionId) " 
                   "FROM ReportConditionFindingOptions GROUP BY ReportId")
    #query to get a reportid with number of conditions
    results = cursor.fetchall()
    condstotal = 0
    for result in results:
        condstotal += result[1]
    #print (condstotal)
    #total number of conditions for reports
    cursor.execute("SELECT (Conditions.Name), COUNT (DISTINCT ReportId)"
                   " from Conditions"
                   " INNER JOIN ReportConditionFindingOptions "
                   "ON Conditions.Id = ReportConditionFindingOptions.ConditionId"
                   " WHERE Name = ? GROUP BY Conditions.Name", c)
    freq_tmp = cursor.fetchone()
    freq = freq_tmp[1]
    #print(freq)
    cond_i = freq/condstotal
    #print(cond_i)
    cursor.execute("SELECT FindingId, COUNT (DISTINCT ReportId) "
                   " FROM ReportConditionFindingOptions "
                   " WHERE FindingId IN (SELECT Id FROM Findings "
                   " WHERE Name = ? ) AND ConditionId IN (SELECT Id FROM Conditions WHERE Name = ?)"
                   " GROUP BY FindingId", f, c)
    find_tmp = cursor.fetchone()
    find = find_tmp[1]
    #print(find)
    find_i = find/freq
    #print(find_i)
    result = cond_i*find_i
    print(result)
    return result



if __name__ == '__main__':
    a = c_i('Fibroadenoma', 'Mass')
    b = c_i('Fibroadenoma', 'Assymetry')
    result_final = a*b
    print(result_final)


