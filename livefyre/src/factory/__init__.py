from datetime import datetime
from livefyre.src.entity.cursor import TimelineCursor


class CursorFactory(object):
    @staticmethod
    def get_topic_stream_cursor(core, topic, limit, date):
        resource = topic.topic_id + ":topicStream"
        return TimelineCursor(core, resource, limit, date)
    
    @staticmethod
    def get_personal_stream_cursor(network, user, limit, date):
        resource = network.get_user_urn(user) +"personalStream"
        return TimelineCursor(network, resource, limit, date)