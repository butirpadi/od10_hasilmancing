from odoo import api, models, fields

class hm_presensi_karyawan(models.Model):
	_name = "hm_presensi_karyawan_rel"

	name = fields.Char('Reference')
	presensi_id = fields.Many2one('hm_presensi', string='Presensi', ondelete='cascade')
	karyawan_id = fields.Many2one('hm_karyawan', string='Karyawan')
	pagi = fields.Boolean('Pagi')
	siang = fields.Boolean('Siang')
	tanggal = fields.Date(related="presensi_id.tanggal",string="Tanggal")