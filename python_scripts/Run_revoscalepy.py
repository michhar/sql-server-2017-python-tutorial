"""
Demostration script for utilizing a remote compute context for 
  SQL Server 2017 in Python using the revoscalepy package.

 Micheleen Harris (michhar@microsoft.com)
 Based on:
   https://docs.microsoft.com/en-us/sql/advanced-analytics/tutorials/use-python-revoscalepy-to-create-model
"""

from revoscalepy.computecontext.RxComputeContext import RxComputeContext
from revoscalepy.computecontext.RxInSqlServer import RxInSqlServer
from revoscalepy.computecontext.RxInSqlServer import RxSqlServerData
from revoscalepy.functions.RxLinMod import rx_lin_mod_ex
from revoscalepy.functions.RxPredict import rx_predict_ex
from revoscalepy.functions.RxSummary import rx_summary
from revoscalepy.utils.RxOptions import RxOptions
from revoscalepy.etl.RxImport import rx_import_datasource

import os

SQL_SERVER_NAME = 'SQLSERVER2017'
DB_NAME = 'Airline_Data_Sample'

def test_linmod_sql():

    # Get environment variables or script variables
    sql_server = os.getenv(ENV_SQL_SERVER_NAME, SQL_SERVER_NAME)
    db_name = os.getenv(ENV_DB_NAME, DB_NAME)

    connectionString = 'Driver=SQL Server;Server=' + sql_server + \
        ';Database=' + db_name + ';Trusted_Connection=True;'

    print("connectionString={0!s}".format(connectionString))

    dataSource = RxSqlServerData(
        sqlQuery = "select top 10 * from airlinedemo", 
        connectionString = connectionString,
        colInfo = { 
            "ArrDelay" : { "type" : "integer" }, 
            "DayOfWeek" : { 
                "type" : "factor", 
                "levels" : ["Monday", "Tuesday", "Wednesday", 
                            "Thursday", "Friday", "Saturday", "Sunday"]
            }
        })

    computeContext = RxInSqlServer(
        connectionString = connectionString,
        numTasks = 1,
        autoCleanup = False
        )

    #
    # import data source to avoid factor levels
    #        
    data = rx_import_datasource(dataSource)
    print(data)

    #
    # run linmod
    #
    linmod = rx_lin_mod_ex("ArrDelay ~ DayOfWeek", data = data, compute_context = computeContext)
    assert (linmod is not None)
    assert (linmod._results is not None)
    print(linmod)

    #
    # predict results
    # 
    data = rx_import_datasource(dataSource)
    del data["ArrDelay"]
    predict = rx_predict_ex(linmod, data = data)
    assert (predict is not None)
    print(predict._results)

    #
    # do a summary
    #
    summary = rx_summary("ArrDelay ~ DayOfWeek", data = dataSource, compute_context = computeContext)
    assert (summary is not None)
    print(summary)

if __name__ == '__main__':
    """Run the test function when script is run"""
    test_linmod_sql()