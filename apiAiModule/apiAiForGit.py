# This class was directly put into my main program lyrics.py so you need little adjustment.
class apiAi:
    def __init__(self,que):
        CLIENT_ACCESS_TOKEN = '' #Enter your access token here.
        ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        requestToAi=ai.text_request()
        requestToAi.lang='en'  # optional, default value equal 'en'
        requestToAi.session_id='' #Enter your ID here.
        requestToAi.query=que
        self.aiResponse=json.loads(requestToAi.getresponse().read())
    def getAiResponse(self):
        return self.aiResponse['result']['metadata']