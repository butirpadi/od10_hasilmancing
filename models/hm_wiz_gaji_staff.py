from odoo import api, models, fields
from pprint import pprint

class hm_wiz_gaji_staff(models.TransientModel):
	_name = 'hm_wiz_gaji_staff'
	_description = 'Wizard Gaji staff'

	name = fields.Char('name', default="Report Gaji Staff")
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir')
	karyawan_id = fields.Many2one('hm_karyawan',string='Karyawan')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')    
	pay_state = fields.Selection([('open', 'Open'),('done', 'Paid')])  
	payroll_ids = fields.Many2many('hm_payroll_staff',string='Gaji staff')
	

	def do_submit_report(self):
		print 'inside do submit report staff'
		# update state
		self.write({
				'state':'open'
			})

		by_karyawan = "true"
		if self.karyawan_id:
			by_karyawan = " karyawan_id = " + str(self.karyawan_id.id) + " "

		by_pay_state = "true"
		if self.pay_state:
			by_pay_state = " state = '" + self.pay_state + "'"

		if len(self.payroll_ids) > 0:
			# clear data sebelumnya
			for old_pres in self.payroll_ids:
				self.payroll_ids = [(3, old_pres.id)]

		# payroll get
		query = ('select * from hm_payroll_staff where tanggal >= %s and tanggal <= %s '
					+ ' and ' + by_karyawan  
					+ ' and ' + by_pay_state  
					+ ' order by tanggal asc')
		
		# get data presensi
		self.env.cr.execute(query,
					(self.tanggal_awal, self.tanggal_akhir))
		for pay in self.env.cr.fetchall():
			self.payroll_ids = [(4,pay[0])]
		self.env.invalidate_all()


