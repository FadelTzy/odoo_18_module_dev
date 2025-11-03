from odoo import fields, models
class MahasiswaData(models.Model):
    _name = 'mahasiswa.data'
    _description = "Mahasiswa Data"

    name = fields.Char(string="Name", required=True)
    nim = fields.Char(string="NIM", required=True, unique=True)
    date_of_birth = fields.Date(string="Date of Birth")
    major = fields.Char(string="Major")
    ipk = fields.Float(string="IPK")
    email = fields.Char(string="Email")
    phone_number = fields.Char(string="Phone Number")
    address = fields.Text(string="Address")
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ], string="Gender")
    fakultas_id = fields.Many2one(
        comodel_name='fakultas.data',
        string="Fakultas",
        ondelete='set null'
    )