import requests


class ResponseRetriever:
    @staticmethod
    def response_retriever(intent, status_id):

        url_intent = 'https://localhost:5001/intent'
        url_response = 'https://localhost:5001/get_prod_response'

        params_intent = {'intent': intent}
        page_intent = requests.get(url=url_intent, params=params_intent, verify=False)
        intent_id = page_intent.json()

        params_response = {'intent_id': intent_id[0][0], 'status_id': status_id}
        page_response = requests.get(url=url_response, params=params_response, verify=False)
        message = page_response.json()

        return message[0][0]


Response = ResponseRetriever()
