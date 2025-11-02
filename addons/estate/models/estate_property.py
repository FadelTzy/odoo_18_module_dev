from odoo import fields,models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
	_name = 'estate.property'
	_description = "estate Property"

	name = fields.Char(required=True)
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date(default=lambda self: fields.Datetime.now() + relativedelta(months=3),copy=False)
	expected_price = fields.Float(required=True)
	selling_price = fields.Float(readonly=True,copy=False)
	bedrooms = fields.Integer(default=2)
	living_area = fields.Integer()
	state = fields.Selection(
                selection=[
                        ('new','New'),
                        ('offer_received','Offer Received'),
                        ('offer_accepted','Offer Accepted'),
                        ('sold','Sold'),
			('cancelled','Cancelled')
                ], default='new', copy=False, required=True
        )
	facades = fields.Integer()
	active = fields.Boolean(default=True)
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection(
		selection=[
			('north','North'), 
			('east','East'),
			('south','South'),
			('west','West'),
		]
	)

