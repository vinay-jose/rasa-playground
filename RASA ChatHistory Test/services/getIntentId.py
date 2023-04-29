import logging
from flask import request
import mysql.connector
import json

logger = logging.getLogger(__name__)


class GetIntentId:
    @classmethod
    def get_intent_id(cls):
        intent_name = request.args['intent']
        mydb = mysql.connector.connect(host='test-hcl.hyreo.com',
                                       database='cb_admin',
                                       user='dbuser',
                                       password='hyr30dbuser')

        sql_command = "select intent_id from intent_master where intent_name = '%s'" % intent_name

        cursor = mydb.cursor()
        cursor.execute(sql_command)
        intent_id = cursor.fetchall()

        return json.dumps(intent_id)


getIntentId = GetIntentId()
