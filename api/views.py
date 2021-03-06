# coding: utf-8

from api import models
from django.contrib.auth.models import User

from api import serializers

import django_filters
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from rest_framework import generics
from rest_framework import filters

from rest_framework.response import Response

from rest_framework.authtoken.models import Token


class TaskFilter(filters.FilterSet):
    end_date_lte = django_filters.DateTimeFilter(
        name="end_date",
        lookup_expr='lte'
    )

    class Meta:
        model = models.Task
        fields = ['id', 'name', 'creation_date',
                  'end_date', 'project__id', 'end_date_lte', 'assigned__id']


"""
TOKEN
"""


class ObtainAuthToken(generics.CreateAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = serializers.AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': str(token.key),
            'id': user.id
        }

        return Response(content)

"""
Users
"""


class UserRetrieve(generics.RetrieveAPIView):
    serializer_class = serializers.UserPublicSerializer

    def get_queryset(self):
        get_object_or_404(User, id=self.kwargs['pk'])
        return models.User.objects.filter(id=self.kwargs['pk'])

"""
PROJECTS
"""


class ProjectListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.ProjectSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id', 'name']

    def get_queryset(self):
        return models.Project.objects.filter(access__user=self.request.user)


class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return models.Project.objects.all()


class ProjectAccessList(generics.ListAPIView):
    serializer_class = serializers.AccessSerializer

    def get_queryset(self):
        # Check if project exist
        project = get_object_or_404(
            models.Project,
            pk=self.kwargs['pk']
        )

        #Check if user have access to this project
        get_object_or_404(
            models.Access,
            project__id=self.kwargs['pk'],
            user__id=self.request.user.id
        )

        return models.Access.objects.filter(project__id=self.kwargs['pk'])


class ProjectTaskList(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer
    filter_class = TaskFilter

    def get_queryset(self):
        # Check if project exist
        project = get_object_or_404(
            models.Project,
            pk=self.kwargs['pk']
        )

        #Check if user have access to this project
        get_object_or_404(
            models.Access,
            project__id=self.kwargs['pk'],
            user__id=self.request.user.id
        )

        return models.Task.objects.filter(project__id=self.kwargs['pk']).order_by('end_date')


class ProjectLabelList(generics.ListAPIView):
    serializer_class = serializers.LabelSerializer

    def get_queryset(self):
        # Check if project exist
        project = get_object_or_404(
            models.Project,
            pk=self.kwargs['pk']
        )

        #Check if user have access to this project
        get_object_or_404(
            models.Access,
            project__id=self.kwargs['pk'],
            user__id=self.request.user.id
        )

        return models.Label.objects.filter(project__id=self.kwargs['pk'])

"""
ACCESS
"""


class AccessListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.AccessSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id']

    def get_queryset(self):
        return models.Access.objects.filter(user=self.request.user)


class AccessRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AccessSerializer

    def get_queryset(self):
        return models.Access.objects.all()


"""
TASKS
"""


class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.TaskSerializer
    filter_class = TaskFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return models.Task.objects.filter(project__access__user=self.request.user)


class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TaskSerializer

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return models.Task.objects.all()

"""
NOTIFICATIONS
"""


class NotificationList(generics.ListAPIView):
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(receiver__id=self.request.user.id)


class NotificationRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        #Check if user have access to this notification
        get_object_or_404(
            models.Notification,
            receiver__id=self.request.user.id,
            pk=self.kwargs['pk']
        )

        return models.Notification.objects.filter(receiver__id=self.request.user.id,pk=self.kwargs['pk'])


"""
LABELS
"""


class LabelListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.LabelSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id', 'name']

    def get_queryset(self):
        return models.Label.objects.all()


class LabelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.LabelSerializer

    def get_queryset(self):
        return models.Label.objects.all()


"""
Files
"""


class FileListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.FileSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id', 'name']

    def get_queryset(self):
        return models.File.objects.all()


class FileRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        return models.File.objects.all()


"""
COMMENTS
"""


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id']

    def get_queryset(self):
        return models.Comment.objects.all()


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.all()


"""
Kanboards
"""


class KanboardListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.KanboardSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id', 'name']

    def get_queryset(self):
        return models.Kanboard.objects.all()


class KanboardRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.KanboardSerializer

    def get_queryset(self):
        return models.Kanboard.objects.all()


"""
Columns of kanboard
"""


class ColumnListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.ColumnSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ['id', 'name']

    def get_queryset(self):
        return models.Column.objects.all()


class ColumnRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ColumnSerializer

    def get_queryset(self):
        return models.Column.objects.all()
