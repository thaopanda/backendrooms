from django.db import models
from Account.models import Host, MyUser

# class PostManager(models.Manager):
#     def search(self, cỉteria):
#         qlookup = ''
#         for i in citeria:

ROOM_TYPE = [
    ('phòng trọ', "phòng trọ"),
    ('chung cư mini', "chung cư mini"),
    ('nhà nguyên căn', "nhà nguyên căn"),
    ('chung cư nguyên căn', "chung cư nguyên căn")
]

RENT_TIME = [
    ('tháng', 'tháng'),
    ('quý', 'quý'),
    ('năm', 'năm'),
]

BATH_ROOM = [
    ('khép kín', "khép kín"),
    ('chung', "chung")
]
KITCHEN = [
    ('khu bếp riêng', "khu bếp riêng"),
    ('khu bếp chung', "khu bếp chung"),
    ('không nấu ăn', "không nấu ăn")
]


class Post(models.Model):
    detailAddress = models.CharField(max_length=200, null=False, blank=False)
    describeAddress = models.CharField(max_length=200)
    roomType = models.CharField(max_length=100, choices=ROOM_TYPE)

    numberOfRoom = models.PositiveIntegerField()

    numberOfRented = models.PositiveIntegerField(default=0)

    price = models.PositiveIntegerField()
    rent_time = models.CharField(max_length=10, choices=RENT_TIME)

    square = models.PositiveIntegerField(default=0)

    withOwner = models.BooleanField()

    bathroomType = models.CharField(max_length=20, choices=BATH_ROOM)
    
    heater = models.BooleanField()

    kitchen = models.CharField(max_length=50, choices=KITCHEN)

    airconditioner = models.BooleanField()

    balcony = models.BooleanField()

    water_price = models.PositiveIntegerField()
    electricity_price = models.PositiveIntegerField()

    other = models.CharField(max_length=200, null=True, blank=True)

    images = models.TextField(blank=True)

    hostName = models.ForeignKey(Host, related_name='hostName', on_delete=models.CASCADE)

    expiredDate = models.DateTimeField()
    
    is_confirmed = models.BooleanField(default=False)

    total_views = models.PositiveIntegerField(default=0)
    
    total_like = models.PositiveIntegerField(default=0)


