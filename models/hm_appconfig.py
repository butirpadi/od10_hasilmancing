from odoo import api, models, fields

class hm_appconfig(models.Model):
    _name = 'hm_appconfig'
    _description = 'Application Config Data'

    name = fields.Char('Name', required=True)
    desc = fields.Char('Nama')
    value = fields.Text('Value')