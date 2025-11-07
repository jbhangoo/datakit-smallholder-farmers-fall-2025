class DiGraphEdge(object):
    def __init__(self, qid: str, **kwargs):
        """
        Create an edge with qid as label and optional attributes
        :param qid:         id of question asked
        :param kwargs:      other question attributes:
                            ['question_user_id', 'question_language', 'question_topic', 'question_sent',
                            'response_user_id', 'response_language', 'response_topic', 'response_sent']
        """
        self.qid = qid
        if kwargs and ('question_sent' in kwargs):
            self.timestamp = kwargs['question_sent']
        else:
            self.timestamp = None

    def __str__(self):
        return f"{self.qid}:\t{self.timestamp})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.qid == other.qid

    def __hash__(self):
        return hash((self.qid, self.timestamp))
