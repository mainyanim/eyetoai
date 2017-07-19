import pyodbc

config = dict(server=   'tcp:eyetoaidevelopment.database.windows.net', # change this to your SQL Server hostname or IP address
              port=      1433,                    # change this to your SQL Server port number [1433 is the default]
              database= 'test',
              username= 'michael',
              password= 'GradioAI7000')


conn_str = ('SERVER={server},{port};'   +
            'DATABASE={database};'      +
            'UID={username};'           +
            'PWD={password}')

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};' +
    conn_str.format(**config)
    )


cursor = conn.cursor()

cursor.execute('SELECT * FROM reports')

for entry in cursor:
    print(entry)