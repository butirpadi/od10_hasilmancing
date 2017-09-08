from odoo import api, models, fields

class hm_payroll_staff(models.Model):
	_name = "hm_payroll_staff"

	name = fields.Char('Name', default="New")
	hm_payroll_staff_id = fields.Many2one('hm_payroll_staff', string="Payroll Staff")
	hm_presensi_karyawan_rel_id = fields.Many2one('hm_presensi_karyawan_rel', string="Payroll Presensi Karyawan Rel")