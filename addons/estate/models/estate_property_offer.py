from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(required=True)
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