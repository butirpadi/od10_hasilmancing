from odoo import api, models, fields

class hm_res_partner(models.Model):
	_inherit = 'res.partner'

	provinsi_id = fields.Many2one('hm_provinsi', string='Provinsi')
	kabupaten_id = fields.Many2one('hm_kabupaten', string='Kabupaten')
	kecamatan_id = fields.Many2one('hm_kecamatan', string='Kecamatan')
	pekerjaan_ids = fields.One2many(
	    'hm_pekerjaan',
	    'partner_id',
	    string='Data Pekerjaan',
	)