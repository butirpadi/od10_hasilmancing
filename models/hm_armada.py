from odoo import api, models, fields

class hm_armada(models.Model):
	_name = "hm_armada"

	name = fields.Char(
	    string='Nopol',
	)
	keterangan = fields.Char(
	    string='Keterangan',
	)

