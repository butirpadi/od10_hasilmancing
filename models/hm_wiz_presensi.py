from odoo import api, models, fields
from pprint import pprint

class hm_wiz_presensi(models.TransientModel):
	_name = 'hm_wiz_presensi'
	_description = 'Wizard Presensi'

	name = fields.Char('name', default="Report Presensi Karyawan")
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir')
	karyawan_id = fields.Many2one('hm_karyawan',string='Karyawan')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')  
	presensi_ids = fields.Many2many('hm_presensi_karyawan_rel',strin='Presensi Karyawan')

	# def do_submit_report(self):
	# 	# update state
	# 	self.write({
	# 			'state':'open'
	# 		})

	# 	by_karyawan = "true"
	# 	if self.karyawan_id:
	# 		by_alat = " karyawan_id = " + str(self.karyawan_id.id) + " "

	# 	if len(self.op_alat_ids) > 0:
	# 		# clear data sebelumnya
	# 		for old_alat in self.op_alat_ids:
	# 			self.op_alat_ids = [(3, old_alat.id)]

	# 	query = ('select * from hm_op_alat where tanggal >= %s and tanggal <= %s and ' 
	# 				+ by_alat + ' and ' + by_galian 
	# 				+ ' order by (tanggal, name) asc')
	# 	# get data op_alat_id
	# 	self.env.cr.execute(query,
	# 				(self.tanggal_awal, self.tanggal_akhir))
	# 	for alat in self.env.cr.fetchall():
	# 		self.op_alat_ids = [(4,alat[0])]

