from kxi.handy import dlog_logger, extract_args, make_engine, assert_integer
import kxi.engine
from kx.wrapper import kdb
import binascii
import _mysql

def acc2id(acc):
    return binascii.crc32(acc.lower()) & 0xffffffff

class AccountServant(kxi.engine.Servant):

    def __init__(self, setting, adapter):
        super(AccountServant, self).__init__(setting, adapter)
        eps = adapter.add_servant('account', self)
        self._db = kdb.Open(self._engine.proxy(setting['account.dbproxy']), escape=_mysql.escape_string)
        self._table_accounts = setting.get('account.table_accounts', 's_accounts')
        self._table_user_accounts = setting.get('account.table_user_accounts', 's_user_accounts')
        self._logger.info("Account Servant Start At %s", eps)

    @assert_integer('uid')
    @extract_args
    def get_accounts(self, uid):
        sql = "SELECT * FROM %s WHERE uid = %d" % (self._table_user_accounts, uid)
        rs = self._db.query(uid, sql)
        if len(rs) == 0:
            return {'ok' : False}
        return {'ok' : True, 'list' : [(row['account'], row['ctime']) for row in rs]}

    @extract_args
    def get_uid(self, account):
        sql = "SELECT * FROM %s WHERE account = '%s'" % (self._table_accounts, self._db.escape(account))
        row = self._db.query_one(acc2id(account), sql)
        if not row:
            return {'ok' : False}
        return {'ok' : True, 'uid' : row['uid'], 'ctime' : row['ctime']}

    @assert_integer('uid')
    @extract_args
    def create_account(self, uid, account):
        accid = acc2id(account)
        sql = kdb.insert_sql(self._table_accounts, {'uid' : uid, 'account' : account}, self._db.escape)
        self._db.execute(accid, sql)
        sql = kdb.insert_sql(self._table_user_accounts, {'uid' : uid, 'account' : account}, self._db.escape)
        self._db.execute(uid, sql)
        return {'ok' : True}

    @assert_integer('uid')
    @extract_args
    def delete_account(self, uid, account):
        accid = acc2id(account)
        sql = "DELETE FROM %s WHERE uid = %d and account = '%s'" % (self._table_accounts, uid, self._db.escape(account))
        n = self._db.execute(accid, sql)
        sql = "DELETE FROM %s WHERE uid = %d and account = '%s'" % (self._table_user_accounts, uid, self._db.escape(account))
        n2 = self._db.execute(uid, sql)
        if n == 0 and n2 == 0:
            return {'ok' : False}
        return {'ok' : True}

def start_server():
    log = dlog_logger('account')
    make_engine('account', AccountServant, logger = log).serve_forever()

if __name__ == '__main__':
    start_server()
