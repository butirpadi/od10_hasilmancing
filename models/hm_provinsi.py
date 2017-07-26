# -*- coding: utf-8 -*-

from odoo import api, models, fields

class hm_provinsi(models.Model):
    _name = 'hm_provinsi'
    _order = 'name'

    name = fields.Char('Nama', required=True)
    kabupaten_ids = fields.One2many('hm_kabupaten', 'provinsi_id', string='Kabupaten')
    