from django.db import models
from Account.models import Host, MyUser

ROOM_TYPE = [
    ('pt', "phòng trọ"),
    ('cc', "chung cư mini"),
    ('n', "nhà nguyên căn"),
    ('ccnc', "chung cư nguyên căn")
]
BATH_ROOM = [
    ('kk', "khép kín"),
    ('c', "chung")
]
KITCHEN = [
    ('r', "khu bếp riêng"),
    ('c', "khu bếp chung"),
    ('k', "không nấu ăn")
]

class Post(models.Model):
    detailAddress = models.CharField(max_length=200, null=False, blank=False)
    describeAddress = models.CharField(max_length=200)
    roomType = models.CharField(max_length=100, choices=ROOM_TYPE)

    numberOfRoom = models.PositiveIntegerField()

    numberOfRented = models.PositiveIntegerField(default=0)

    price = models.PositiveIntegerField()

    square = models.PositiveIntegerField

    withOwner = models.BooleanField()

    bathroomType = models.CharField(max_length=20, choices=BATH_ROOM)
    #nóng lạnh
    kitchen = models.CharField(max_length=50, choices=KITCHEN)

    airconditioner = models.BooleanField()
    balcony = models.BooleanField()

    utility = models.PositiveIntegerField()

    other = models.CharField(max_length=200, null=True, blank=True)
    images = models.ImageField(blank=True)
    host_id = models.ForeignKey(Host, related_name='host_of_this_post', on_delete=models.CASCADE)
    hostName = models.CharField(max_length=50)
    hostPhoneNumber = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)


