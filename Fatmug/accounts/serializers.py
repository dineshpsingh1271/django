from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    # Serializer for user signup
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        # Custom validation to check if the email is already in use
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        # Create a new user with a hashed password
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        # Generate a token for the new user
        Token.objects.create(user=user)

        return user


class CurrentUserPostsSerializer(serializers.ModelSerializer):
    # Serializer for displaying current user's posts
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post_detail", queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "posts"]
