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
	presensi_ids = fields.Many2many('hm_presensi',strin='Presensi Karyawan')
	presensi_rel_ids = fields.Many2many('hm_presensi_karyawan_rel',strin='Presensi Karyawan rel')

	def do_submit_report(self):
		print 'inside do submit report'
		# update state
		self.write({
				'state':'open'
			})

		by_karyawan = "true"
		if self.karyawan_id:
			by_karyawan = " karyawan_id = " + str(self.karyawan_id.id) + " "

		if len(self.presensi_ids) > 0:
			# clear data sebelumnya
			for old_pres in self.presensi_ids:
				self.presensi_ids = [(3, old_pres.id)]

			for old_pres_rel in self.presensi_rel_ids:
				self.presensi_rel_ids = [(3, old_pres_rel.id)]

		# presensi
		query_pres = ('select * from hm_presensi where tanggal >= %s and tanggal <= %s order by tanggal asc')

		# presensi rel
		query_pres_rel = ('select * from hm_presensi_karyawan_rel where tanggal_org >= %s and tanggal_org <= %s and ' 
					+ by_karyawan  
					+ ' order by tanggal_org asc')
		
		# get data presensi
		self.env.cr.execute(query_pres,
					(self.tanggal_awal, self.tanggal_akhir))
		for pres in self.env.cr.fetchall():
			self.presensi_ids = [(4,pres[0])]
		self.env.invalidate_all()

		# get data presensi rel
		self.env.cr.execute(query_pres_rel,
					(self.tanggal_awal, self.tanggal_akhir))
		for pres_rel in self.env.cr.fetchall():
			self.presensi_rel_ids = [(4,pres_rel[0])]
		self.env.invalidate_all()

