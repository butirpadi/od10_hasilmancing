from odoo import api, models, fields
from datetime import datetime

class hm_gaji_pegawai(models.Model):
	_name = "hm_gaji_pegawai"

	tanggal = fields.Char('Tanggal', default=datetime.today())
	pay_week_id = 
	