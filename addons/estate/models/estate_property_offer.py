from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(required=True)
    validity = fields.Integer(
        string="Validity (days)",
        required=True,
        default=7
    )

    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_set_date_deadline',
        string="Deadline",
        store=True
    )
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        required=True,
        default='refused'
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string="Property",
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        ondelete='set null',
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.type_id",
        store=True
    )
    # _sql_constraints = [
    #     ('offer_price_positive','CHECK(price > 0)','The offer price must be positive.'),	
    # ]
       
    @api.constrains('price')
    def _check_offer_price_positive(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The offer price must be positive.")

    def action_accept(self):
        for record in self:
            if record.property_id and record.price < record.property_id.expected_price * 0.9:
                raise ValidationError("The offer price must be at least 90% of the expected price.")
            if record.property_id.state == "sold":
                raise UserError("Cannot accept an offer on a sold property.")
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "sold"
            record.status = "accepted"
            record.property_id.selling_price = record.price
        return True    

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True	

    @api.depends('validity', 'create_date','date_deadline')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)
    
    def _set_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
                delta = offer.date_deadline - base_date
                offer.validity = delta.days
    
    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        property_record = self.env['estate.property'].browse(property_id)
        existing_offers = self.search([('property_id', '=', property_id)])
        for offer in existing_offers:
            if vals.get('price') and vals['price'] <= offer.price:
                raise ValidationError("New offer price must be higher than existing offers for the same property.")
        
        property_record.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)