from odoo import models, fields, api
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='type_id',
        string="Properties"
    )
    property_count = fields.Integer(
        string="Number of Properties",
        compute='_compute_property_count'
    )
    _sql_constraints = [
        ('unique_nama','unique(name)','The Type name must be unique')
    ]
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string="Offers"
    )
    offer_count = fields.Integer(
        string="Number of Offers",
        compute='_compute_offer_count'
    )
    @api.depends('property_ids')
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
