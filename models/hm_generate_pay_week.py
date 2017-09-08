from odoo import api, models, fields

class hm_generate_pay_week(models.Model):
	_name = "hm_generate_pay_week"

	name = fields.Char('Tahun')
	pay_week_ids = fields.One2many('hm_pay_week','generate_id')