from django.conf import settings

import happybase


class HBaseClient:
    conn = None

    @classmethod
    def get_connection(cls):
        if cls.conn:
            return cls.conn
        cls.conn = happybase.Connection(host='192.168.33.10',port=9090,autoconnect=True,protocol = 'compact')
        return cls.conn