from odoo import api, models, fields
from pprint import pprint

class hm_wiz_report_alat(models.TransientModel):
	_name = 'hm_wiz_report_alat'
	_description = 'Wizard Report Alat Berat'

	name = fields.Char('name', default="Report Operasional Alat Berat")
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir')
	alat_berat_id = fields.Many2one('hm_alat_berat',string='Alat Berat')
	galian_id = fields.Many2one('hm_galian',string='Lokasi Galian')
	op_alat_ids = fields.Many2many('hm_op_alat',string='Data Operasional Alat Berat')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')  

	def do_submit_report(self):
		# update state
		self.write({
				'state':'open'
			})

		by_alat = "true"
		if self.alat_berat_id:
			by_alat = " alat_berat_id = " + str(self.alat_berat_id.id) + " "

		by_galian = "true"
		if self.galian_id:
			by_galian = " lokasi_galian_id = " + str(self.galian_id.id) + " "

		if len(self.op_alat_ids) > 0:
			# clear data sebelumnya
			for old_alat in self.op_alat_ids:
				self.op_alat_ids = [(3, old_alat.id)]

		query = ('select * from hm_op_alat where tanggal >= %s and tanggal <= %s and ' 
					+ by_alat + ' and ' + by_galian 
					+ ' order by (tanggal, name) asc')
		# get data op_alat_id
		self.env.cr.execute(query,
					(self.tanggal_awal, self.tanggal_akhir))
		for alat in self.env.cr.fetchall():
			self.op_alat_ids = [(4,alat[0])]


	# def action_get_data_report(self):
	# 	res = self.env['hm_op_alat'].search([('tanggal','>=',self.tanggal_awal),('tanggal','<=',self.tanggal_akhir)], order="tanggal asc")
	# 	self.data_kas = res
	# 	debet = sum(map(lambda x:x.debet,res))
	# 	kredit = sum(map(lambda x:x.kredit,res))
	# 	self.total_saldo = debet-kredit
	# 	self.state = 'open'

	# def hm_wiz_jurnal_print(self):
	# 	print 'print wizard jurnal'