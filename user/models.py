from django.db import models


class UserManager(models.Manager):
    def create_user(self, username, email, password, phone_number):
        user = self.create(username=username, email=email, password=password, phone_number=phone_number)
        return user

    def has_email(self, email):
        """
        判断该email是否已存在
        :param email: str(email)
        :return: boolean()
        """
        # noinspection PyBroadException
        try:
            self.get(email=email)
            return True
        except:
            return False

    def has_phone_number(self, phone_number):
        """
        判断该电话是否已存在
        :param phone_number: str(phone_number)
        :return: boolean()
        """
        # noinspection PyBroadException
        try:
            self.get(phone_number=phone_number)
            return True
        except:
            return False


class TeamManager(models.Manager):
    def create_team(self, team_name):
        team = self.create(team_name=team_name)
        return team


class TeamUserManager(models.Manager):
    def create_team_user(self, team_id, user_id, user_permission='0'):
        new_team_user = self.create(team_id=team_id, user_id=user_id, user_permission=user_permission)
        return new_team_user


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_id = models.AutoField(primary_key=True)
    objects = TeamManager()

    def __str__(self):
        return self.team_name


class User(models.Model):
    avatar = models.CharField(max_length=500, null=True)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=11)
    user_id = models.AutoField(primary_key=True)
    active_team = models.IntegerField(null=True)
    objects = UserManager()

    def __str__(self):
        return self.email


class TeamUser(models.Model):
    user_rights = (
        ('0', 'general_user'),
        ('1', 'administrator'),
        ('2', 'super_administrator'),
    )
    team_id = models.IntegerField()
    user_id = models.IntegerField()
    user_permission = models.CharField(max_length=2, choices=user_rights, default='0')
    objects = TeamUserManager()
