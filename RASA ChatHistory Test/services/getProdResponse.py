import logging
from flask import request
import mysql.connector
import json

logger = logging.getLogger(__name__)


class GetProdResponse:
    @classmethod
    def get_prod_response(cls):
        # method to get details of specific response
        intent_id = request.args.get('intent_id')
        status_id = request.args.get('status_id')
        sql_command = "select irs.response,ice.status_id from live_intent_response irs " \
                      "join (select ir.intent_response_id,iss.status_id from live_intent_response ir " \
                      "left join live_intent_status iss on iss.intent_response_id = ir.intent_response_id  " \
                      "where  ir.intent_id = %s) as" \
                      " ice on irs.intent_response_id = ice.intent_response_id where ice.status_id = %s " \
                      "or ice.status_id is null;" % (intent_id, status_id)

        mydb = mysql.connector.connect(host='test-hcl.hyreo.com',
                                       database='cb_admin',
                                       user='dbuser',
                                       password='hyr30dbuser')

        # cur = mysql.connection.cursor()
        cursor = mydb.cursor()
        resultValue = cursor.execute(sql_command)
        # if resultValue != None:
        user_details = cursor.fetchall()

        # return render_template('users.html',userDetails=userDetails)
        return json.dumps(user_details)


getProdResponse = GetProdResponse()
