from odoo import api, models, fields

class hm_alat_berat(models.Model):
	_name = "hm_alat_berat"

	name = fields.Char('Nama')
	kode = fields.Char('Kode')