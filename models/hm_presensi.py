from odoo import api, models, fields

class hm_presensi(models.Model):
	_name = "hm_presensi"
	_order = "tanggal desc"

	name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
    					index=True, select=True, default='New')
	tanggal = fields.Date('Tanggal')

	# karyawan_rel_ids = fields.One2many('hm_presensi_karyawan_rel', 'presensi_id', 
										# string="Presensi Karyawan", compute='_compute_get_karyawan')

	karyawan_rel_ids = fields.One2many('hm_presensi_karyawan_rel', 'presensi_id', 
										string="Presensi Karyawan")

	# def _compute_get_karyawan(self):
	# 	for prs in self:
	# 		kary = self.env['hm_karyawan'].search([('jabatan','=','STF')])
	# 		for dt in kary:
	# 			dt_kary['karyawan_id'] = dt.id 
	# 			dt_kary['pagi'] = False
	# 			dt_kary['siang'] = False
	# 		prs.karyawan_rel_ids = dt_kary

	def generate_data_karyawan(self):
		print 'fill karyawan'
		kary = self.env['hm_karyawan'].search([('jabatan','=','STF')])
		dt_kary = []
		for dt in kary:
			dt_kary.append({
					'karyawan_id' : dt.id,
					'pagi' : False,
					'siang' : False
				})
		self.karyawan_rel_ids = dt_kary

	@api.model
	def create(self, vals):
		if vals.get('name', ('New')) == ('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('hm.presensi.seq') or ('New')
	
		result = super(hm_presensi, self).create(vals)
		return result

	# @api.model
	# def unlink(self):
	# 	self.env['hm_presensi_karyawan_rel'].search([('presensi_id', '=', self.id)]).unlink()
	# 	return super('hm_presensi', self).unlink()