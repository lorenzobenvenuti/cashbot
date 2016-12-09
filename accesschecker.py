class AccessChecker(object):

    def is_allowed(self, fuser):
        pass


class WhitelistChecker(object):

    def __init__(self, user_ids):
        self._user_ids = user_ids

    def is_allowed(self, user):
        return user.id in self._user_ids
