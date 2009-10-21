import ldap

from django.contrib.auth.models import User, Group, check_password
from django.contrib.auth.backends import RemoteUserBackend
from django.conf import settings

class ActiveDirectoryBackend:
    def authenticate(self,username=None,password=None):
        if not self.is_valid(username,password):
            return None

        try:
            user = User.objects.get(username=username)
            if not check_password(password, user.password):
                # pass is diff, update
                user.set_password(password)

            return user
        except User.DoesNotExist:
            # create the user
            pass

        # get user info
        l = self.ldap_connect(username, password)
        result = l.search_ext_s(settings.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, 
                "sAMAccountName=%s" % username, settings.AD_SEARCH_FIELDS)[0][1]
        l.unbind_s()

        kwargs = {}
        # givenName == First Name
        if result.has_key('givenName'):
            kwargs['first_name'] = result['givenName'][0]

        # sn == Last Name (Surname)
        if result.has_key('sn'):
            kwargs['last_name'] = result['sn'][0]

        # mail == Email Address
        if result.has_key('mail'):
            kwargs['email'] = result['mail'][0]
    
        user = User(username=username,**kwargs)
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save()
        return user

    def ldap_connect(self, username, password):
        """
        Creates connection to ldap, user in charge of unbinding
        """
        con = ldap.initialize(settings.AD_LDAP_URL)
        binddn = "%s@%s" % (username, settings.AD_NT4_DOMAIN)
        con.simple_bind_s(binddn, password)
        return con

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def is_valid (self, username=None,password=None):
        # Disallowing null or blank string as password
        # as per comment: http://www.djangosnippets.org/snippets/501/#c868
        if password == None or password == '':
            return False

        try:
            l = self.ldap_connect(username, password)
            l.unbind_s()
            return True
        except ldap.LDAPError:
            return False
        except Exception, e:
            pass

        return False


class UWRemoteUserBackend(RemoteUserBackend):
    """
    Checks for the $REMOTE_USER var and if it exists, trusts the user was authenticated successfully. If the user is successfully authenticated, but doesn't exist it will be created and added to the "Everyone" group, to get some default permissions.
    """
    def configure_user(self, user):
        """
        Gives the user some default permissions.
        """
        everyone = Group.objects.get_or_create('Everyone')
        user.groups.add(everyone)
        return user
