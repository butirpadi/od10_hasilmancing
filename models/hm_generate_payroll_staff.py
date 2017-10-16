from odoo import api, models, fields
import datetime
from pprint import pprint

class hm_generate_payroll_staff(models.Model):
	_name = "hm_generate_payroll_staff"

	tanggal =fields.Date('Tanggal', required=True,default=datetime.date.today())
	pay_staff_ids = fields.One2many('hm_payroll_staff','generate_id',string="Data Gaji Staff")
	name = fields.Many2one('hm_generate_pay_week',string="Tahun", required=True)
	bulan = fields.Selection([ 
				(1,'JANUARI'),
				(2, 'FEBRUARI'),
				(3, 'MARET'),
				(4, 'ARPIL'),
				(5, 'MEI'),
				(6, 'JUNI'),
				(7, 'JULI'),
				(8, 'AGUSTUS'),
				(9, 'SEPTEMBER'),
				(10, 'OKTOBER'),
				(11, 'NOVEMBER'),
				(12, 'DESEMBER'),
				],required=True)
	pay_week_id = fields.Many2one('hm_pay_week',String="Minggu", required=True)
	pay_day = fields.Date('Pay Day')
	pay_day_start = fields.Date('Pay Day Start')
	pay_day_end = fields.Date('Pay Day End')
	pay_day_range = fields.Char('Tanggal Pembayaran')

	pay_day_temp = fields.Date('Pay Day')
	pay_day_start_temp = fields.Date('Pay Day Start')
	pay_day_end_temp = fields.Date('Pay Day End')

	is_generate = fields.Boolean('Is Generated', default=False)

	_sql_constraints = [
        ('name__bulan__pay_week_id_constraint_2', 'unique(name, bulan, pay_week_id)', 'Data telah tersedia sebelumnya.'),
    ]

	@api.onchange('pay_week_id')
	def pay_week_change(self):
		print 'pay week change'
		self.set_pay_day()

	@api.onchange('bulan')
	def bulan_change(self):
		print 'bulan change'
		self.set_pay_day()
		# clear pay week id
		self.pay_week_id = None

	@api.onchange('name')
	def name_change(self):
		print 'name change'
		self.set_pay_day()
		# clear pay week id
		self.pay_week_id = None
		
	def set_pay_day(self):
		self.pay_day = self.pay_week_id.tanggal 
		self.pay_day_start = self.pay_week_id.awal
		self.pay_day_end = self.pay_week_id.akhir

		self.pay_day_temp = self.pay_week_id.tanggal 
		self.pay_day_start_temp = self.pay_week_id.awal
		self.pay_day_end_temp = self.pay_week_id.akhir

		self.pay_day_range = str(self.pay_week_id.awal) + " - " + str(self.pay_week_id.akhir)


	def generate_gaji_staff(self):
		if not self.is_generate:
			# get data staff
			staffs = self.env['hm_karyawan'].search([('jabatan','=','STF')])
			print 'generate gaji staff'
			payroll_staffs = []
			for x in staffs:
				new_payroll_staff = {
						'karyawan_id' : x.id,
						'periode_awal':self.pay_week_id.awal,
						'periode_akhir':self.pay_week_id.akhir,
						'tanggal':self.pay_day,
					}
				payroll_staffs.append(new_payroll_staff)
				# print 'Karyawan id : ' + str(x.id)
				# print 'Tanggal awal ' + str(self.pay_week_id.awal)
				# print 'Tanggal akhir ' + str(self.pay_week_id.akhir)
				# print '------------------------------------------'
			# pprint(payroll_staffs)
			
			self.pay_staff_ids = payroll_staffs
			self.is_generate = True

			# generate payrol drier
			for pay in self.pay_staff_ids:
				print 'generate payrol staff : ' + str(pay.karyawan_id.name)
				pay.onchange_karyawan_id()
				pay.show_presensi()
				print '-------------------------------------------------'
		else:
			print 'Data has been generated'

	@api.model
	def create(self, vals):
		print 'Update Tanggal Gaji & Tanggal Pembayaran '
		print 'tanggal gaji ' + str(self.pay_day)
		print 'tanggal awal ' + str(self.pay_day_start)
		print 'tanggal akhir ' + str(self.pay_day_end)
		# update tanggal
		vals.update({
				'pay_day_temp' : vals['pay_day'],
				'pay_day_start_temp' : vals['pay_day_start'],
				'pay_day_end_temp' : vals['pay_day_end'],
			})
		return super(hm_generate_payroll_staff, self).create(vals)



