from datetime import datetime
import datetime
from datetime import date

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import Customer
from models import CustomerMiniForm
from models import CustomerForm
from models import CustomerTotalForm
from models import CustomerList
from models import CustomerShortFormList
from models import CustomerShortForm
from models import GetCustIDForm
from models import ReturnCustOrderForm

from models import ItemForm
from models import ItemTotalForm
from models import Item
from models import ItemList
from models import ItemDateForm

from models import OrderForm
from models import Order
from models import DailyOrder
from models import OrderFormOutput
import logging
import heapq
CUST_GET_REQUEST = endpoints.ResourceContainer(
message_types.VoidMessage,
custId=messages.IntegerField(1,variant=messages.Variant.INT32)
)
ITEM_GET_REQUEST = endpoints.ResourceContainer(
message_types.VoidMessage,
itemId=messages.IntegerField(1,variant=messages.Variant.INT32)
)

@endpoints.api(name='dairymanagement', version='v1')
class DairyManagemnetApi(remote.Service):

	def _copyCustomerToForm(self, cust):
		cf = CustomerForm()
		if cust:
			for field in cf.all_fields():
				if hasattr(cust, field.name):
					if(field.name == "key"):
						setattr(cf,field.name,(getattr(cust,field.name)).id())
					else:
						setattr(cf, field.name, getattr(cust, field.name))
			cf.check_initialized()
		return cf



	@endpoints.method(CustomerMiniForm,CustomerForm,
	path='customer/addcustomer', http_method='GET', name='createCustomer')
	def createCustomer(self,request):
		c_id = Customer.allocate_ids(size=1)[0]
		c_key = ndb.Key(Customer, c_id)
		data = {field.name: getattr(request, field.name) for field in request.all_fields()}
		data['key'] = c_key
		query = Customer.query().filter(Customer.mobileNumber == data['mobileNumber'])
		entity = query.get()
		if entity:
			raise Exception('unique_property must have a unique value!')
		Customer(**data).put()
		return 0
		#return self._copyCustomerToForm(c_key.get())

	@endpoints.method(CUST_GET_REQUEST,CustomerForm,
	path='customer/{custId}', http_method='GET', name='getCustomer')
	def getCustomer(self, request):
		key = ndb.Key(Customer,request.custId)
		cust = key.get()
		return self._copyCustomerToForm(cust)


# - - - - - -  Item - - - - - - - - -  -


	def _copyItemToForm(self, item):
		it = ItemForm()
		if item:
			for field in it.all_fields():
				if hasattr(item, field.name):
					setattr(it, field.name, getattr(item, field.name))
			it.check_initialized()
		return it

	@endpoints.method(ItemForm,ItemForm,
	path='item/createItem', http_method='GET', name='createItem')
	def createItem(self,request):
		i_id = Item.allocate_ids(size=1)[0]
		i_key = ndb.Key(Item, i_id)
		data = {field.name: getattr(request, field.name) for field in request.all_fields()}
		data['key'] = i_key
		Item(**data).put()
		return self._copyItemToForm(i_key.get())

	@endpoints.method(ITEM_GET_REQUEST,ItemForm,
	path='Item/{itemId}', http_method='GET', name='getItem')
	def getItem(self, request):
		key = ndb.Key(Item,request.itemId)
		item = key.get()
		return self._copyItemToForm(item)

	#------ Order -----------------------------------------------------------
	def _copyOrderToForm(self, order):
		of = OrderFormOutput()
		if order:
			for field in of.all_fields():
				if hasattr(order, field.name):
					if field.name in ('custId','itemId','key'):
						setattr(of, field.name, (getattr(order, field.name)).integer_id())
					else:
						if field.name in ('orderDate'):

							setattr(of, field.name, datetime.datetime.strftime(getattr(order, field.name), '%m/%d/%y'))
						else:
							setattr(of, field.name, getattr(order, field.name))
			of.check_initialized()
		return of

	def update_customer_credit_debit_total(self,data,c_key,credit):
		x = Customer.query(ancestor = data['custId'])
		obj = c_key.get()
		obj.debit = obj.debit + data['orderPrice']
		obj.credit = obj.credit + credit
		obj.total = obj.debit - obj.credit
		obj.put()

	def update_dailyorder(self,data):
		query = DailyOrder.query(ndb.AND(DailyOrder.custId == data['custId'] , DailyOrder.itemId == data['itemId'], DailyOrder.orderDate == data['orderDate']))
		logging.debug(data['orderDate'])
		logging.debug(query)
		x=0
		for q in query:
			data['key'] = q.key
			data['itemQuantity'] = q.itemQuantity + data['itemQuantity']
			data['orderPrice'] = q.orderPrice + data['orderPrice']
			data['orderDate'] = q.orderDate
			x=1
		if x:
			print "i"

		else:
			print "else mai hun"
			do_id = Item.allocate_ids(size=1)[0]
			do_key = ndb.Key(DailyOrder, do_id)
			data['key'] = do_key
		DailyOrder(**data).put()



	@endpoints.method(OrderForm,OrderFormOutput,
	path='order/placeOrder', http_method='GET', name='placeOrder')
	def placeOrder(self,request):
		print "creating Customer"
		o_id = Item.allocate_ids(size=1)[0]

		data = {}
		for field in request.all_fields():
			if field.name == 'custId':

				data[field.name] = ndb.Key(Customer,getattr(request,field.name))
				c_key = ndb.Key(Customer,getattr(request,field.name))


				o_key = ndb.Key(Order, o_id,parent=data[field.name])

			else:
				if field.name == 'itemId':

					data[field.name] = ndb.Key(Item,getattr(request,field.name))
					obj = (ndb.Key(Item,getattr(request,field.name))).get()

					price = obj.itemPrice

				else:
					if field.name == 'credit':
						credit = getattr(request,field.name)
					else:
						if field.name == 'orderDate':
							if getattr(request,field.name) == None:
								data[field.name] = datetime.datetime.now()
							else:
								data[field.name] = datetime.datetime.strptime(getattr(request,field.name), '%m/%d/%y:%H:%M:%S')
						else:
							data[field.name] = getattr(request,field.name)
		data['key'] = o_key

		data['orderPrice'] = price * data['itemQuantity']
		if(data['itemQuantity']>=0):
			Order(**data).put()

			self.update_customer_credit_debit_total(data,c_key,credit)

			self.update_dailyorder(data)


		return self._copyOrderToForm(o_key.get())

	def _copyItemsToForm(self, item):
		"""Copy relevant fields from Profile to ProfileForm."""
		# copy relevant fields from Profile to ProfileForm
		it = ItemTotalForm()
		if item:
			for field in it.all_fields():
				if hasattr(item, field.name):
					if (field.name == 'key'):
						setattr(it,field.name,(getattr(item,field.name)).id())
					else:

				# convert t-shirt string to Enum; just copy others
						setattr(it, field.name, getattr(item, field.name))
			it.check_initialized()
		return it


	@endpoints.method(message_types.VoidMessage,ItemList,
	path='/getItemList', http_method='GET', name='getItemList')
	def getItemList(self,request):
		print "creating Customer"
		c = []
		query1 = Item.query()
		print query1
		entity1 = query1.get()
		print entity1
		for q in query1:
			c.append(self._copyItemsToForm(q))
		return ItemList(itemList=c)

	def _copyCustomerTotalDetailToForm(self, cust):
		cf = CustomerTotalForm()
		if cust:
			for field in cf.all_fields():
				if hasattr(cust, field.name):
					if(field.name == "custId"):
						setattr(cf,field.name,(getattr(cust,field.name)).id())
					else:
						setattr(cf, field.name, getattr(cust, field.name))
			#setattr(cf,'itemQuantity',2.5)
			cf.check_initialized()
		return cf

	@endpoints.method(message_types.VoidMessage,CustomerList,
	path='/getCustomerList', http_method='GET', name='getCustomerList')
	def getCustomerList(self,request):
		c = []
		query1 = Customer.query()
		for q in query1:
			setattr(q,'custId',q.key)
			c.append(self._copyCustomerTotalDetailToForm(q))

		return CustomerList(customerList=c)

	def _copyCustomerItemQuantityToForm(self, cust):
		cf = CustomerTotalForm()
		if cust:
			for field in cf.all_fields():
				if hasattr(cust, field.name):
					if(field.name in ("key","custId","itemId")):
						setattr(cf,field.name,(getattr(cust,field.name)).id())
					else:
						setattr(cf, field.name, getattr(cust, field.name))
			#setattr(cf,'itemQuantity',2.5)
			cf.check_initialized()
		return cf
	@endpoints.method(ItemDateForm,CustomerShortFormList,
	path='/getDateSpecifiedPurchase', http_method='GET', name='getDateSpecifiedPurchase')
	def getDateSpecifiedPurchase(self,request):
		c = []
		d = []
		z = []
		dategiven=0
		data = {}
		query1 = Customer.query()
		entity1 = query1.get()
		for field in request.all_fields():
			if (field.name == 'itemId'):
				data[field.name] = ndb.Key(Item,getattr(request,field.name))
			else:
				data[field.name] = getattr(request,field.name)
		logging.debug('date')
		logging.debug(data['date'])
		for q in query1:
			if(data['date'] != None):
				logging.debug(data['date'])
				f = datetime.datetime.strptime(data['date'], '%m/%d/%y').date()
			else:
				d = DailyOrder.query(DailyOrder.custId == q.key,projection = [DailyOrder.orderDate])
				for x in d:
					z.append(x.orderDate)
				f = heapq.nlargest(1,z)
				if f:
					f = f[0]
			y = -1
			logging.debug(f)
			if f:
				q1 = DailyOrder.query(ndb.AND(DailyOrder.custId == q.key, DailyOrder.orderDate == f, DailyOrder.itemId == data['itemId']),projection = [DailyOrder.itemQuantity])
				for q2 in q1:
					y = q2.itemQuantity
			else:
				y = -1
			logging.debug('query resulet')
			logging.debug(q1)
			for q2 in q1:
					logging.debug(q2)
			setattr(q,'itemQuantity',float(y))
			setattr(q,'custId',q.key)
			c.append(self._copyCustomerItemQuantityToForm(q))
			z = []


		return CustomerShortFormList(custItemQuantityList=c)


	@endpoints.method(GetCustIDForm,ReturnCustOrderForm,
	path='/getOrder', http_method='GET', name='getOrder')
	def getOrder(self,request):
		data = {}
		c = []
		for field in request.all_fields():
			data[field.name] = getattr(request,field.name)

		orders = Order.query(Order.custId == ndb.Key(Customer,data['custId']))
		for order in orders:
			setattr(order,'itemName',(Item.query(Item.key == order.itemId, projection = [Item.itemName])).get().itemName)
			logging.debug(order)
			logging.debug(order.key)
			c.append(self._copyOrderToForm(order))
			logging.debug(c)
		return ReturnCustOrderForm(orderList=c)




api = endpoints.api_server([DairyManagemnetApi]) # register API
