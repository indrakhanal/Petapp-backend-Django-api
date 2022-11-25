from dataclasses import fields
# from xml.etree.ElementTree import Comment
from rest_framework import serializers
from . models import PetDetailPost, UserProfile, WishListItem, Comment


class PetsPostSerializers(serializers.ModelSerializer):
    # img_url = serializers.SerializerMethodField()

    class Meta:
        model=PetDetailPost
        fields = '__all__'

    def get_img_url(self, obj):
        image1 = self.context['request'].build_absolute_uri(obj.image1.url)
        image2 = self.context['request'].build_absolute_uri(obj.image2.url)
        try:
            image3 = self.context['request'].build_absolute_uri(obj.image3.url)
        # if not image3:
        except:
            image3 = None
        try:
            image4 = self.context['request'].build_absolute_uri(obj.image4.url)
        except:
            image4=None
        return image1, image2, image3, image4

    # def validate(self, attrs):
    #     return super().validate(attrs)

class WishListSearializers(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = '__all__'



class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'