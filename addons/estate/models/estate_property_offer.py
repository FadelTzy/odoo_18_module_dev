from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

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
    
    def action_accept(self):
        for record in self:
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