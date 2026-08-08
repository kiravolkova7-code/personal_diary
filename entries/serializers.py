from rest_framework import serializers
from .models import User, Entry

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class EntrySerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(source="user", read_only=True)

    class Meta:
        model = Entry
        fields = '__all__'
