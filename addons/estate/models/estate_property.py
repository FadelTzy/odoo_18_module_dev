from odoo import fields,models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
	_name = 'estate.property'
	_description = "estate Property"

	name = fields.Char("Title",required=True)
	user_id = fields.Many2one(
		comodel_name='res.users',
		string="Salesman",
		ondelete='set null',
		default=lambda self: self.env.user
	)
	buyer_id = fields.Many2one(
		comodel_name='res.partner',
		string="Buyer",
		ondelete='set null',
		copy=False
	)
	tag_ids = fields.Many2many(
		'estate.property.tag',
		string="Property Tags"
	)
	offer_ids = fields.One2many(
		'estate.property.offer',
		'property_id',
		string="Offers"
	)
	description = fields.Text()
	postcode = fields.Char("Postcode")
	date_availability = fields.Date(default=lambda self: fields.Datetime.now() + relativedelta(months=3),copy=False,string="Available From")
	expected_price = fields.Float(required=True,string="Expected Price")
	selling_price = fields.Float(readonly=True,copy=False,string="Selling Price")
	bedrooms = fields.Integer(default=2,string="Bedrooms")
	living_area = fields.Integer(string="Living Area (sqm)")
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
	type_id = fields.Many2one(
		comodel_name='estate.property.type',
		string="Property Type",
		ondelete='set null'
	)

