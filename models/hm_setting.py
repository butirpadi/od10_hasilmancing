from odoo import api, models, fields, exceptions
from datetime import date, timedelta
import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import datetime
from pprint import pprint
from calendar import monthrange

class hm_setting(models.Model):
	_name = "hm_setting"

	name = fields.Char('Nama', Default="Setting")
	kode_driver_prefix = fields.Char('Kode driver prefix')
	kode_driver_counter = fields.Integer('Kode driver counter')
	kode_staff_prefix = fields.Char('Kode staff prefix')
	kode_staff_counter = fields.Integer('Kode staff counter')
	catatan_slip_gaji = fields.Text('Catatan slip gaji')
	printer_surat_jalan = fields.Char('Printer surat jalan')
	generate_pay_day_tahun = fields.Char('Generate Minggu Gajian')
	# generate_pay_day_day = fields.Char('Hari Gaji')
	generate_pay_day_day = fields.Selection([
				(0, 'SENIN'), 
				(1,'SELASA'),
				(2, 'RABU'),
				(3, 'KAMIS'),
				(4, 'JUMAT'),
				(5, 'SABTU'),
				(6, 'MINGGU')
				],string="Hari Gaji")
	# printer_invoice = fields.Text('Catatan slip gaji')


	# Generate Pay Day/Week
	def action_generate_pay_week(self):
		# print 'generate pay week'		
		nama_bulan = ['Januari', 
						'Februari', 
						'Maret', 
						'April', 
						'Mei', 
						'Juni', 
						'Juli', 
						'Agustus', 
						'September', 
						'Oktober', 
						'November', 
						'Desember' 
						]

		# create generate_pay_week data
		year=int(self.generate_pay_day_tahun)

		# cek apakah tahun tersebut telah di generate
		if self.env['hm_generate_pay_week'].search([('name', '=', year )]):
			# return {'value':{},'warning':{'title':'warning','message':'Error, Pay Week pada tahun ' + str(year) + ' telah di generated sebelumnya.'}}
			print 'Gagal Generate karena data sudah ada'
			raise exceptions.except_orm((''),('Error, data pay week tahun ' + str(year) + ' telah digenerate sebelumnya.'))
		else:
			hm_generate = self.env['hm_generate_pay_week'].create({
					'name':year
				})
			for x in range(1,13): #for in month/bulan
				# print '---------------------------------'
				# print 'X : ' + str(x)
				# print 'bulan int : ' + str(x-1)
				# print 'bulan str : ' + nama_bulan[x-1]
				# print '---------------------------------'
				dt_start=datetime.datetime(year,x,1)
				dt_end=datetime.datetime(year,x,monthrange(year, x)[1])
				rr = rrule.rrule(rrule.WEEKLY,byweekday=self.generate_pay_day_day,dtstart=dt_start)
				data_pay_day = rr.between(dt_start,dt_end,inc=True)
				mgg_ke = 1
				# print 'bulan ke : ' + str(x)
				for day in data_pay_day: #for per tanggal
					# print 'crete data........................'
					self.env['hm_pay_week'].create({
							'tanggal' : day,
							'awal' : day - timedelta(days=7), 
							'akhir' : day - timedelta(days=1),
							'tahun' : year,
							'pay_day' : self.generate_pay_day_day,
							'pay_day_str' : dict(self._fields['generate_pay_day_day'].selection).get(self.generate_pay_day_day),
							'minggu_ke' : mgg_ke,
							'minggu_ke_str' : 'Minggu ' + str(mgg_ke),
							'name' : 'Minggu ' + str(mgg_ke),
							'bulan_int' : x-1,
							'bulan_str' : nama_bulan[x-1],
							'generate_id' : hm_generate.id
						})					
					mgg_ke += 1
					# print 'data created ----------------------'
					# print day 
					# print '----------------------------------'