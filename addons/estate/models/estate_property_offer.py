from odoo import models, fields, api
from datetime import timedelta
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