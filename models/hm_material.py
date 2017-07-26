# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools

class hm_material(models.Model):
    _inherit = "product.template"

    tipe_product = fields.Selection([('spr', 'Sparepart'), ('mtr','Material')], 'Tipe', required=True)
    empfield = fields.Char('Empty Field')

    @api.model
    def create(self, vals):
        # newrow = super(product_template,self).create(vals)
        ## set jika tipe adalah part maka type adalah cons
        print('tipe produk : ' + vals['tipe_product'])
        if vals['tipe_product'] == 'spr':
            vals.update({'type':'consu'})
            vals.update({'purchase_ok':True})
            vals.update({'sale_ok':False})
        elif vals['tipe_product'] == 'mtr':
            vals.update({'type':'product'})
            vals.update({'sale_ok':True})
            vals.update({'purchase_ok':False})

        newrow = super(hm_material,self).create(vals)

        # Tambahkan quantity jika produk jenis Material
        if vals['tipe_product'] == 'mtr':
            print('Add initial quantity')
            print('=======================================')
            Inventory = self.env['stock.inventory']
            inventory = Inventory.create({
                'name': ('INV: %s') % tools.ustr(newrow.name),
                'filter': 'product',
                'product_id': newrow.id,
                'location_id': 15,
                # 'lot_id': wizard.lot_id.id,
                'line_ids': [(0, 0, {
                           'product_qty': 10,
                           'location_id': 15,
                           'product_id': newrow.id,
                           # 'product_uom_id': self.product_id.uom_id.id,
                           'theoretical_qty': 10,
                           # 'prod_lot_id': self.lot_id.id,
                    })],
            })
            inventory.action_done()

        return newrow

    @api.multi 
    def unlink(self):
        print 'delete data material'
        # cek stock
        # jika stock nya 10 maka boleh di delete
        total_stock = 0
        jumlah_stock_line = 0
        prods = self.product_variant_id
        for prod in prods:
            for stock in prod.stock_ids:
                total_stock = sum(map(lambda f: f.product_qty, stock.line_ids))
                jumlah_stock_line = len(stock.line_ids)
                print 'total stok : ' + str(total_stock)
                print 'jumlah stok_line : ' + str(jumlah_stock_line)

        if jumlah_stock_line == 1:
            # delete stock line & stock terlebih dahulu
            for prod in prods:
                for stock in prod.stock_ids:
                    for line in stock.line_ids:
                        # delete stock_inventory_line
                        self.env.cr.execute("delete from stock_inventory_line where id = " + str(line.id))
                    
                    for move in stock.move_ids:
                        for quant in move.quant_ids:
                            # delete stock_quant_move_rel
                            self.env.cr.execute("delete from stock_quant_move_rel where quant_id = " + str(quant.id))
                            # delete stock_quant                    
                            self.env.cr.execute("delete from stock_quant where id = " + str(quant.id))
                            # delete from stock_move
                            self.env.cr.execute("delete from stock_move where id = " + str(move.id))                    
                    # delete stock_inventory
                    self.env.cr.execute("delete from stock_inventory where id = " + str(stock.id))


        return super(hm_material,self).unlink()


