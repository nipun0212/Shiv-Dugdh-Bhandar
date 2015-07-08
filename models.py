import httplib
import endpoints
from protorpc import messages
from protorpc import message_types
from google.appengine.ext import ndb
import datetime


class Customer(ndb.Model):
    """Profile -- User profile hkjobject"""
    userName = ndb.StringProperty(required=True)
    mainEmail = ndb.StringProperty()
    mobileNumber = ndb.StringProperty(required=True)
    credit = ndb.FloatProperty(required=True,default=0.0)
    debit = ndb.FloatProperty(required=True,default=0.0)
    total = ndb.FloatProperty(required=True,default=0.0)
    timestamp = ndb.DateTimeProperty(default=datetime.datetime.now())

class CustomerMiniForm(messages.Message):
    """ProfileMiniForm -- update njnProfile form message"""
    userName = messages.StringField(1)
    mobileNumber = messages.StringField(2)
    mainEmail = messages.StringField(3)
    credit = messages.FloatField(4,default=0.0)
    debit = messages.FloatField(5,default=0.0)


class CustomerForm(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    key = messages.IntegerField(1)
    userName = messages.StringField(2)
    mainEmail = messages.StringField(3)
    mobileNumber = messages.StringField(4)
    credit = messages.FloatField(5,default=0.0)
    debit = messages.FloatField(6,default=0.0)

class CustomerTotalForm(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    custId = messages.IntegerField(1)
    userName = messages.StringField(2)
    mainEmail = messages.StringField(3)
    mobileNumber = messages.StringField(4)
    credit = messages.FloatField(5,default=0.0)
    debit = messages.FloatField(6,default=0.0)
    itemQuantity = messages.FloatField(7,default=0.0)

class ItemTotalForm(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    key = messages.IntegerField(1)
    itemName = messages.StringField(2)
    itemPrice = messages.FloatField(3,variant=messages.Variant.FLOAT)



class CustomerList(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    customerList = messages.MessageField(CustomerTotalForm, 1, repeated=True)

class Item(ndb.Model):
    itemName = ndb.StringProperty(required=True)
    itemPrice = ndb.FloatProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now=True)


class ItemForm(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    itemName = messages.StringField(1)
    itemPrice = messages.FloatField(2,variant=messages.Variant.FLOAT)

class ItemList(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    itemList = messages.MessageField(ItemTotalForm, 1, repeated=True)


class Order(ndb.Model):
    custId = ndb.KeyProperty(Customer,required=True)
    itemId = ndb.KeyProperty(Item,required=True)
    itemQuantity = ndb.FloatProperty(required=True)
    orderDate = ndb.DateTimeProperty(default = datetime.datetime.now())
    orderPrice = ndb.FloatProperty(required=True)

class OrderFormOutput(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    custId = messages.IntegerField(1)
    itemId = messages.IntegerField(2)
    itemQuantity = messages.FloatField(3)
    itemName = messages.StringField(4)
    orderDate = messages.StringField(5)
    orderPrice = messages.FloatField(6)
    orderId = messages.IntegerField(7)
    credit = messages.FloatField(8,default=0.0)
    key = messages.IntegerField(9)
class OrderForm(messages.Message):
    """ProfileForm -- Profile nm,outbound form message"""
    custId = messages.IntegerField(1)
    itemId = messages.IntegerField(2)
    itemQuantity = messages.FloatField(3)
    credit = messages.FloatField(4,default=0.0)
    orderDate = messages.StringField(5)

class DailyOrder(ndb.Model):
    custId = ndb.KeyProperty(Customer,required=True)
    itemId = ndb.KeyProperty(Item,required=True)
    itemQuantity = ndb.FloatProperty(required=True)
    orderDate = ndb.DateProperty(required=True)
    orderPrice = ndb.FloatProperty(required=True)

class Profile(ndb.Model):
    """Profile -- User profile object"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    teeShirtSize = ndb.StringProperty(default='NOT_SPECIFIED')
    conferenceKeysToAttend = ndb.StringProperty(repeated=True)

class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- update Profile form message"""
    displayName = messages.StringField(1)
    teeShirtSize = messages.EnumField('TeeShirtSize', 2)

class ProfileForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    teeShirtSize = messages.EnumField('TeeShirtSize', 3)
    conferenceKeysToAttend = messages.StringField(4, repeated=True)

class CustomerShortForm(messages.Message):
    custId = messages.IntegerField(1)
    itemQuantity = messages.FloatField(2)

class CustomerShortFormList(messages.Message):
    custItemQuantityList = messages.MessageField(CustomerTotalForm,1,repeated=True)


class ItemDateForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    itemId = messages.IntegerField(1,required=True)
    date = messages.StringField(2)

class ReturnCustOrderForm(messages.Message):
    orderList = messages.MessageField(OrderFormOutput,1,repeated=True)

class GetCustIDForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    custId = messages.IntegerField(1,required=True)