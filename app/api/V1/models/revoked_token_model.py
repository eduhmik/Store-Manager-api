class RevokedTokenModel():

    revoked = []
    def __init__(self, id, jti):
        self.id = id
        self.jti = jti

    def add(self):
        new = dict(
            id = self.id,
            jti = self.jti
        )
        self.revoked.append(new)
        return new

    @classmethod
    def is_jti_blacklisted(self, jti):
        find_jti = [j for j in RevokedTokenModel.revoked if j['jti'] == jti]
        return bool(find_jti)