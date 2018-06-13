from django.db import models


class ProjectManager(models.Manager):
    def create_project(self, project_name, team_id):
        project = self.create(project_name=project_name, team_id=team_id)
        return project


class ProjectListManager(models.Manager):
    def create_project_list(self, list_name, project_id):
        new_project_list = self.create(list_name=list_name, project_id=project_id)
        return new_project_list


class ListItemManager(models.Manager):
    def create_list_item(self, title, project_list_id):
        """
        新建list item
        :param title: str(标题)
        :param project_list_id: int(关联的列表id)
        :return: ListItem(新生成的ListItem)
        """
        new_list_item = self.create(title=title, project_list_id=project_list_id)
        return new_list_item


class ItemDetailManager(models.Manager):
    def create_item_detail(self, value, list_item_id):
        new_item_detail = self.create(value=value, list_item_id=list_item_id)
        return new_item_detail


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    team_id = models.IntegerField()
    project_id = models.AutoField(primary_key=True)
    objects = ProjectManager()

    def __str__(self):
        return self.project_name


class ProjectList(models.Model):
    list_name = models.CharField(max_length=200)
    project_id = models.IntegerField()
    project_list_id = models.AutoField(primary_key=True)
    objects = ProjectListManager()

    def __str__(self):
        return self.list_name


class ListItem(models.Model):
    title = models.CharField(max_length=200)
    project_list_id = models.IntegerField()
    list_item_id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    user_id = models.IntegerField(null=True)
    deadline = models.DateField(null=True)
    description = models.CharField(max_length=1000, null=True)
    complete_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(null=True)
    objects = ListItemManager()

    def __str__(self):
        return self.title


class ItemDetail(models.Model):
    value = models.CharField(max_length=500)
    list_item_id = models.IntegerField()
    item_detail_id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    complete_time = models.DateTimeField(null=True)
    objects = ItemDetailManager()

    def __str__(self):
        return self.value
