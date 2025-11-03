from odoo import fields,models,api
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
	total_area = fields.Float(compute='_compute_total_area', string="Total Area (sqm)")
	best_price = fields.Float(compute='_compute_best_price', string="Best Offer Price")	
	@api.depends('living_area','garden_area')
	def _compute_total_area(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area
	
	@api.depends('offer_ids')
	def _compute_best_price(self):
		for record in self:
			# Filter hanya offer yang status-nya 'accepted'
			accepted_offers = record.offer_ids.filtered(lambda o: o.status == 'accepted')

			if accepted_offers:
				record.best_price = max(accepted_offers.mapped('price'))
			else:
				record.best_price = 0.0

	@api.onchange('garden')
	def _onchange_garden(self):
		if self.garden == True:
			self.garden_area = 10
			self.garden_orientation = 'north'
		
		
		else:
			self.garden_area = 0
			self.garden_orientation = False