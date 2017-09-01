from odoo import api, models, fields
import datetime
from pprint import pprint

class hm_generate_pay_driver(models.Model):
	_name = "hm_generate_pay_driver"

	tanggal =fields.Date('Tanggal', required=True,default=datetime.date.today())
	pay_driver_ids = fields.One2many('hm_payroll_driver','generate_id',string="Data Gaji")
	name = fields.Many2one('hm_generate_pay_week',string="Tahun", required=True)
	bulan = fields.Selection([ 
				(0,'JANUARI'),
				(1, 'FEBRUARI'),
				(2, 'MARET'),
				(3, 'ARPIL'),
				(4, 'MEI'),
				(5, 'JUNI'),
				(6, 'JULI'),
				(7, 'AGUSTUS'),
				(8, 'SEPTEMBER'),
				(9, 'OKTOBER'),
				(10, 'NOVEMBER'),
				(11, 'DESEMBER'),
				],required=True)
	pay_week_id = fields.Many2one('hm_pay_week',String="Minggu", required=True)
	pay_day = fields.Date('Pay Day')
	pay_day_start = fields.Date('Pay Day Start')
	pay_day_end = fields.Date('Pay Day End')
	pay_day_range = fields.Char('Tanggal Pembayaran')
	# bulan_str = fields.Char('Bulan')
	# bulan_int = fields.Integer('BulanInt')
	# minggu_ke_int = fields.Integer('MingguInt')
	# minggu_ke_str = fields.Char('Minggu')

	@api.onchange('pay_week_id')
	def pay_week_change(self):
		print 'pay week change'
		self.pay_day = self.pay_week_id.tanggal 
		self.pay_day_start = self.pay_week_id.awal
		self.pay_day_end = self.pay_week_id.akhir
		self.pay_day_range = str(self.pay_week_id.awal) + " - " + str(self.pay_week_id.akhir)


	def generate_gaji_driver(self):
		# get data driver
		drivers = self.env['hm_karyawan'].search([('jabatan','=','DRV')])
		print 'generate gaji driver'
		payroll_drivers = []
		for x in drivers:
			new_payroll_driver = {
					'karyawan_id' : x.id,
					'periode_awal':self.pay_week_id.awal,
					'periode_akhir':self.pay_week_id.akhir,
				}
			payroll_drivers.append(new_payroll_driver)
			# print 'Karyawan id : ' + str(x.id)
			# print 'Tanggal awal ' + str(self.pay_week_id.awal)
			# print 'Tanggal akhir ' + str(self.pay_week_id.akhir)
			# print '------------------------------------------'
		# pprint(payroll_drivers)
		
		self.pay_driver_ids = payroll_drivers

