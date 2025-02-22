from api.models import User, Profile, Todos,chatMessage
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile  
        fields = ['id','user','full_name','image']   

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match"})
        return attrs

    def create(self, attrs):
        user = User.objects.create(
            username=attrs['username'],
            email=attrs['email'],
        )
        user.set_password(attrs['password'])
        user.save()
        return user
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos 
        fields = ["id","user","title","completed","date"]



class chatMessageSerializer(serializers.ModelSerializer):

    reciever_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)
    class Meta:
        model = chatMessage
        fields = ["id","user","sender","sender_profile","reciever","reciever_profile","message","is_read","date"]



     

        
        
