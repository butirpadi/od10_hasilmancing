# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hm_galian(models.Model):
    _name = 'hm_galian'
    _order = 'name'
    
    name = fields.Char('Nama', required=True)
    alamat = fields.Char('Alamat')
    kecamatan_id = fields.Many2one(
        'hm_kecamatan',
        string='Kecamatan',
    )
    kabupaten_id = fields.Many2one(
        'hm_kabupaten',
        string='Kabupaten',
    )
    provinsi_id = fields.Many2one(
        'hm_provinsi',
        string='Provinsi',
    )
