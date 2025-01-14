from full_cost import settings

if hasattr(settings, 'AUTH_LDAP_SERVER_URI'):
    import ldap


class LDAP:
    def __init__(self):
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI'):
            try:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
                ldap.set_option(ldap.OPT_REFERRALS, 0)
                self.connect = ldap.initialize('ldaps://ldap-slave1.cemes.fr')
                self.connect.simple_bind_s()
            except:
                self.connect = None

    def get_group_ldap(self, ldap_user):
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI') and self.connect is not None:

            infos = self.get_user_info(ldap_user.username)
            if infos is not None:
                group_id = infos['gidNumber'][0].decode()
                group = self.get_group(group_id)
                return group

    def get_group_ldap_last_name(self, ldap_last_name):
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI') and self.connect is not None:
            infos = self.get_user_info_last_name(ldap_last_name)
            if infos is not None:
                group_id = infos['gidNumber'][0].decode()
                group = self.get_group(group_id)
                return group

    def get_user_info(self, username):
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI') and self.connect is not None:
            r = self.connect.search_s('ou=People,dc=cemes,dc=fr', ldap.SCOPE_SUBTREE, f'(uid={username})', [])
            if r:
                return r[0][1]

    def get_user_info_last_name(self, last_name):
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI') and self.connect is not None:
            r = self.connect.search_s('ou=People,dc=cemes,dc=fr', ldap.SCOPE_SUBTREE, f'(sn={last_name})', [])
            if r:
                return r[0][1]

    def get_group(self, group_id):
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI') and self.connect is not None:
            r = self.connect.search_s('ou=Group,dc=cemes,dc=fr', ldap.SCOPE_SUBTREE, f'(gidNumber={group_id})', [])
            if r:
                return dict(short=r[0][1]['cn'][0].decode(), long=r[0][1]['description'][0].decode())



