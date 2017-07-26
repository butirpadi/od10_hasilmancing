# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hm_kecamatan(models.Model):
    _name = 'hm_kecamatan'
    _order = 'name'
    
    name = fields.Char('Nama', required=True)
    kabupaten_id = fields.Many2one('hm_kabupaten', 'Kabupaten', ondelete='cascade')
