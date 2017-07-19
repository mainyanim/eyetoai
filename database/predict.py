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

def get_c_i(c):
    cursor.execute("SELECT Max(ReportId) FROM ReportConditionFindingOptions")
    total = cursor.fetchval()
    cursor.execute("SELECT COUNT (Conditions.Name) from Conditions INNER JOIN ReportConditionFindingOptions ON Conditions.Id = ReportConditionFindingOptions.ConditionId WHERE Name = ?", c)
    freq = cursor.fetchval()
    print("{0} / {1} = {2}".format(freq, total, freq / total))

def get_f_j(f):
    cursor.execute("SELECT COUNT(*) FROM Findings")
    total = cursor.fetchval()
    cursor.execute("SELECT COUNT(*) FROM Findings WHERE Name=?", f)
    freq = cursor.fetchval()
    print("{0} / {1} = {2}".format(freq, total, freq / total))

if __name__ == '__main__':
    get_c_i('Fibroadenoma')
    get_f_j('Mass')

