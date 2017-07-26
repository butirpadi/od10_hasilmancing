from odoo import models, api, fields 

class hm_pekerjaan(models.Model):
	_name = "hm_pekerjaan"

	name = fields.Char('Nama', required=True)
	partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='cascade')
	tahun = fields.Char('Tahun',size=4, required=True)
	alamat = fields.Char('Alamat')
	provinsi_id = fields.Many2one('hm_provinsi', 'Provinsi')
	kabupaten_id = fields.Many2one('hm_kabupaten', 'Kabupaten')
	kecamatan_id = fields.Many2one('hm_kecamatan', 'Kecamatan')