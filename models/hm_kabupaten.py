# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hm_kabupaten(models.Model):
    _name = 'hm_kabupaten'
    _order = 'name'

    name = fields.Char('Nama', required=True)
    kecamatan_ids = fields.One2many('hm_kecamatan', 'kabupaten_id', 'Kecamatan')
    provinsi_id = fields.Many2one('hm_provinsi', 'Provinsi', ondelete='cascade')
