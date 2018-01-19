# Interacting with SQL Server 2016/2017

There are two ways shown here of interacting with the SQL Server instance running in a Docker container (macOS or Windows).

Using `sqlcmd` from the command line, for example, starting the command line tool to write SQL queries against any database in the container/server:

    sqlcmd -S localhost -U sa -P $SQL_PASS

Writing Python code leveraging the `pyodbc` package, for example, adding data to the Employees table in a parameterized way:

```python
print ('Inserting a new row into table')
# Insert Query
tsql = "INSERT INTO Employees (Name, Location) VALUES (?,?);"
with cursor.execute(tsql, 'Humpty Dumpty', 'Sweden'):
    print('Successfully Inserted!')
```

See, [Ref](https://github.com/mkleehammer/pyodbc/wiki/Getting-started) for more getting started ideas with `pyodbc`.