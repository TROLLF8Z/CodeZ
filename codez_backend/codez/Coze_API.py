import os, time, random
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType

class CodeZ_AIJudge:
    def __init__(self):
        self.coze_api_token = os.getenv('COZE_API_TOKEN')
        self.coze_api_base = COZE_CN_BASE_URL

        self.coze = Coze(auth=TokenAuth(token = self.coze_api_token), base_url = self.coze_api_base)
        self.bot_id = '7493925240091934760'
        self.user_id = str(random.randint(100000, 999999))

    def chat(self, question, standard_answer, answer):
        tmptxt = '问题：%s\n题库内答案：%s\n学生作答：%s' % (question, standard_answer, answer)
        chat_poll = self.coze.chat.create_and_poll(
            bot_id=self.bot_id,
            user_id=self.user_id,
            additional_messages=[
                Message.build_user_question_text(tmptxt),
            ],
        )
        return chat_poll.messages