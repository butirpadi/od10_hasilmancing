from odoo import models, api, fields 

class hm_product_selection(models.TransientModel):
	_name = "hm_product_selection"

	name = fields.Char('Nama', required=True)
	ref_id = fields.Integer('ID')