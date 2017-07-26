# -*- coding: utf-8 -*-
from odoo import http

# class /home/eries/odoo10/addons/hasilmancing(http.Controller):
#     @http.route('//home/eries/odoo10/addons/hasilmancing//home/eries/odoo10/addons/hasilmancing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/eries/odoo10/addons/hasilmancing//home/eries/odoo10/addons/hasilmancing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/eries/odoo10/addons/hasilmancing.listing', {
#             'root': '//home/eries/odoo10/addons/hasilmancing//home/eries/odoo10/addons/hasilmancing',
#             'objects': http.request.env['/home/eries/odoo10/addons/hasilmancing./home/eries/odoo10/addons/hasilmancing'].search([]),
#         })

#     @http.route('//home/eries/odoo10/addons/hasilmancing//home/eries/odoo10/addons/hasilmancing/objects/<model("/home/eries/odoo10/addons/hasilmancing./home/eries/odoo10/addons/hasilmancing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/eries/odoo10/addons/hasilmancing.object', {
#             'object': obj
#         })