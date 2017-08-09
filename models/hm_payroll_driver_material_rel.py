from odoo import api, models, fields
from pprint import pprint

class hm_payroll_driver_material_rel(models.Model):
	_name = "hm_payroll_driver_material_rel"

	payroll_id = fields.Many2one('hm_payroll_driver', string='Payroll', ondelete='cascade')
	material_id = fields.Many2one('product.template', string='Material')
	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				])
	vol = fields.Float('Volume')
	netto = fields.Float('Netto')
	rit = fields.Float('Rit')
	harga = fields.Float('Harga')
	jumlah = fields.Float(compute='_compute_amount', string='Jumlah', store=True)
	pekerjaan_id = fields.Many2one('hm_pekerjaan',string='Pekerjaan')
	

	@api.depends('vol', 'netto', 'rit', 'harga')
	def _compute_amount(self):
		# print 'on compute amount'
		for line in self:
			if line.kalkulasi == 'ritase':
				# print 'inside ritase'
				line.update({
					'jumlah': line.rit * line.harga
	            })
			elif line.kalkulasi == 'tonase':
				# print 'inside tonase'
				line.update({
	                'jumlah': line.netto * line.harga
	            })
			elif line.kalkulasi == 'kubikasi':
				# print 'inside kubikasi'
				line.update({
	                'jumlah': line.vol * line.harga
	            })