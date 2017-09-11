from odoo import api, models, fields

class hm_payroll_presensi_rel(models.Model):
	_name = "hm_payroll_presensi_rel"

	name = fields.Char('Name', default="New")
	hm_payroll_staff_id = fields.Many2one('hm_payroll_staff', string="Payroll Staff", ondelete='cascade') 
	hm_presensi_karyawan_rel_id = fields.Many2one('hm_presensi_karyawan_rel', string="Payroll Presensi Karyawan Rel")
	tanggal = fields.Date('Tanggal')
	karyawan_id = fields.Many2one('hm_karyawan', string="Karyawan")
	pagi = fields.Boolean('Pagi')
	siang = fields.Boolean('Siang')