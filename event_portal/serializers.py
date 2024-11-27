from rest_framework import serializers
from .models import *


class EventQuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question.question', read_only=True)
    help_text = serializers.CharField(source='question.help_text', read_only=True)
    is_faq = serializers.BooleanField(source='question.is_faq', read_only=True)

    class Meta:
        model = EventQuestion
        fields = ['question', 'help_text', 'is_faq']

class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    posted_by_full_name = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    event_wallpaper = serializers.SerializerMethodField()
    event_question = EventQuestionSerializer(many=True, read_only=True)  # Add event questions

    class Meta:
        model = Event
        fields = '__all__'

    def get_event_wallpaper(self, obj):
        request = self.context.get('request')
        if obj.event_wallpaper:
            return request.build_absolute_uri(obj.event_wallpaper.url)
        return None  # or return a default URL if needed

