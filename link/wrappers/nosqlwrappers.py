from link import Wrapper
from link.utils import list_to_dataframe

class NoSqlConnectionWrapper(Wrapper):
    """
    wraps a database connection and extends the functionality
    to do tasks like put queries into dataframes
    """
    def __init__(self, wrap_name = None, **kwargs):
        
        if kwargs:
            self.__dict__.update(kwargs)

        #get the connection and pass it to wrapper os the wrapped object
        connection = self.create_connection()
        super(NoSqlConnectionWrapper, self).__init__(wrap_name, connection)
   
    def set_table(self, table):
        self.table = table
    
    def get_current_table(self, table=None):
        """
        """
        if table:
            return table
        if self.table:
            return self.table
        raise Exception("No table defined or no default table")

    def get(self, key, table=None):
        """
        get the row or rows from a table (could do cool things with rows by
        allowing for regex or searches
        """
        pass
    
    def put(self, key, column, value, table=None):
        """
        put a key or keys back to the nosqldb
        """
        pass

    def _host_to_hostport(self, host):
        """
        turn your host into a (host, port) combo 
        """
        #need to figure out the standard db port
        (ret_host, ret_port) = ("", 8080)
        host_info = host.split(":")
        if len(host_info)>1:
            ret_port = host_info[1]
        ret_host = host_info[0]
        return (ret_host, int(ret_port))

    def create_connection(self):
        """
        Override this function to create a depending on the type
        of database

        :returns: connection to the database you want to use
        """
        pass


class HbaseNoSqlConnectionWrapper(NoSqlConnectionWrapper):
    """
    A connection wrapper for a sqlite database
    """
    import happybase 
    #from hbase import Hbase 

    def __init__(self, wrap_name=None, host=None, version=None):
        """
        A connection for a SqlLiteDb.  Requires that sqlite3 is
        installed into python

        :param host: the host:port of the hbase thrift server
        """
        self.version = version
        (self.host, self.port) = self._host_to_hostport(host)
        
        # TODO: Where would one configure the default port for link
        super(HbaseNoSqlConnectionWrapper, self).__init__(wrap_name=wrap_name)

    def create_connection(self):
        """
        Override the create_connection from the DbConnectionWrapper
        class which get's called in it's initializer
        """
        #from thrift.transport.TSocket import TSocket
        #from thrift.transport.TTransport import TBufferedTransport
        #from thrift.protocol import TBinaryProtocol
        #from hbase import Hbase 

        #transport = TBufferedTransport(TSocket(self.host,self.port))
        #transport.open()
        #protocol = TBinaryProtocol.TBinaryProtocol(transport)

        return self.happybase.Connection(self.host,
                                         port=self.port,compat=self.version)

    #def increment(self, row, column, amount=1, table=None):
        #"""
        #Increment a column by some amount
        #"""
        #table = self.get_current_table(table)
        #self._wrapped.atomicIncrement(table, row, column, amount)

    #def get(self, row, columns=None, table=None):
        #"""
        #get the row or rows from a table (could do cool things with rows by
        #allowing for regex or searches
        #"""
        #table = self.get_current_table(table)
        #return self._wrapped.getRowWithColumns(table, row, columns=columns)
    
    #def put(self, row, column, value, table=None):
        #"""
        #put a key or keys back to the nosqldb.  Should support dictionary
        #updates or multiple mutations
        #"""
        #table = self.get_current_table(table)
        #mutation = self.Hbase.Mutation(column=column,value=value)
        #return self._wrapped.mutateRow(table, row, [mutation])

    def __call__(self):
        """
        Run's the command line sqlite application
        """
        self.run_command('hbase shell')
