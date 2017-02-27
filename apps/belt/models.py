from __future__ import unicode_literals

from django.db import models
from ..login.models import User
from django.core.exceptions import ObjectDoesNotExist


class ItemManager(models.Manager):

	errors = []

	def create_product(self, data, userid):
		self.errors = []

		if not userid or not User.objects.filter(id=userid).exists():
			self.errors.append("Invalid User")
		else:
			user = User.objects.get(id=userid)

		print user.id, user.alias, user.name

		if 'name' not in data or len(data['name']) < 4:
			self.errors.append("Item/Product must be more than 3 characters")
		elif not self.filter(name=data['name']).exists() and not self.errors:
			# self.create(name=data['name'], added_by=user, user=user)
			item = self.create(name=data['name'], added_by=user)
			item.user.add(user)


		return self.errors

	def add_product(self, itemid, userid):
		self.errors = []

		if not int(userid) or not User.objects.filter(id=userid).exists():
			self.errors.append("Invalid User")
		else:
			user = User.objects.get( id=userid )

		if not self.errors:
			try:
				item = self.get(id=itemid)
				user.wishlist.add(item)
			except ObjectDoesNotExist:
				self.errors.append("Invalid Item")

		return self.errors


class Item(models.Model):

	name = models.CharField(max_length=255)
	added_by = models.ForeignKey(User, related_name="items_added")
	created_at = models.DateTimeField( auto_now_add=True )
	updated_at = models.DateTimeField( auto_now=True )
	user = models.ManyToManyField(User, related_name="wishlist")

	objects = ItemManager()
