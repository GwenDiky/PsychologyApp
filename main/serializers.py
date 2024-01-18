# import io
#
# from rest_framework import serializers
# from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
# from .models import Mood
#

# class MoodModel:
#     def __init__(self, title):
#         self.title = title

# class MoodSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length = 20)
#
#     def create(self, validated_data):
#         return MoodSerializer.objects.create(**validated_data)
#
#     def update(self, instance, validated_data): # instance - текущий экземпляр
#         instance.title = validated_data.get('title', instance.title)
#         instance.save()
#         return instance

# class MoodSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Mood
#         fields = "__all__"

# def encode():
#     model = MoodModel("Воодушевление")
#     model_sr = MoodSerializer(model)
#     print(model_sr.data, type(model_sr.data))
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     streams = io.BytesIO(b'{"title":"Воодушевление"}')
#     data = JSONParser().parse(streams)
#     serializer = MoodSerializer(data = data)
#     serializer.is_valid()
#     print(serializer.validated_data)
