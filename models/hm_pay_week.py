from odoo import api, models, fields
from datetime import date, timedelta
import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import datetime
from pprint import pprint
from calendar import monthrange

class hm_pay_week(models.Model):
	_name = "hm_pay_week"
	_order = 'tahun, bulan_int, minggu_ke'

	# name = fields.Char('Name',default="Generate Pay Week")
	name = fields.Char('Name')
	minggu_ke = fields.Integer('Urut')
	minggu_ke_str = fields.Char('Urut str')
	tanggal = fields.Date('tanggal')
	awal = fields.Date('awal')
	akhir = fields.Date('akhir')
	tahun = fields.Char('Tahun')
	bulan_int = fields.Integer('Bulan Int')
	bulan_str = fields.Char('Bulan')
	pay_day = fields.Selection([
				(0, 'SENIN'), 
				(1,'SELASA'),
				(2, 'RABU'),
				(3, 'KAMIS'),
				(4, 'JUMAT'),
				(5, 'SABTU'),
				(6, 'MINGGU')
				],required=True, default=0)
	pay_day_str = fields.Char('Pay day str')
	generate_id = fields.Many2one('hm_generate_pay_week', required=True,ondelete='cascade')
