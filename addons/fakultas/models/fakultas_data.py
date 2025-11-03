from odoo import fields, models
class FakultasData(models.Model):
    _name = 'fakultas.data'
    _description = "Fakultas Data"

    name = fields.Char(string="Name", required=True)
    kode_fakultas = fields.Char(string="Kode Fakultas", required=True, unique=True)
    dekan = fields.Char(string="Dekan")
    jumlah_prodi = fields.Integer(string="Jumlah Program Studi")
    alamat = fields.Text(string="Alamat")
    email = fields.Char(string="Email")
    phone_number = fields.Char(string="Phone Number")
    website = fields.Char(string="Website")