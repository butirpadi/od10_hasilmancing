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

	_sql_constraints = [
        ('tanggal_constraint', 'unique(tanggal)', 'Data telah tersedia sebelumnya.'),
    ]

	is_generated = fields.Boolean('Is Generated', default=False)

	def generate_data_karyawan(self):
		if not self.is_generated:
			print 'fill karyawan'
			kary = self.env['hm_karyawan'].search([('jabatan','=','STF')])
			dt_kary = []
			for dt in kary:
				dt_kary.append({
					'karyawan_id' : dt.id,
					'pagi' : False,
					'siang' : False,
					'tanggal_org' : self.tanggal
				})
				
			self.karyawan_rel_ids = dt_kary
			self.is_generated = True
		else:
			print 'Data has been generated'

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