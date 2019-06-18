# -*- coding: utf-8 -*-
from odoo import models, fields, api, osv, tools
from openerp.tools.translate import _
from odoo.exceptions import UserError, ValidationError, Warning
import logging, datetime
_logger = logging.getLogger(__name__)


class Bail(models.Model):
    _name = 'psdc_project.bail'
    _rec_name = 'number'
    number = fields.Char(
        string='N de Fianza',
        required=True)
    issue_date = fields.Date(
        string='Fecha de Emisión',
        required=True)
    expired_at = fields.Date(
        string='Fecha de Vencimiento',
        required=True)
    insurer_id = fields.Many2one(
        'res.partner',
        string='Aseguradora',
        required=True,
        domain=[('is_insurer', '=', 'True')])
    endorsement_ids = fields.One2many(
        'psdc_project.endorsement',
        'bail_id',
        string='Endozos')
    project_id = fields.Many2one(
        'project.project',
        string='Proyecto')

    def _validate_current_date(self, date, limit=datetime.datetime.now().date(), message='fecha actual'):
        if date < limit:
            raise ValidationError("La fecha ingresada es inválida, no puede ser menor a la {0}".format(message))

    @api.onchange('expired_at')
    @api.depends('issue_date')
    def _onchange_end_on(self):
        if self.expired_at:
            self._validate_current_date(date=self.expired_at, limit=self.issue_date, message='fecha de emisión')

    @api.model
    def create(self, vals):
        """Override the default create method"""
        start_on = vals.get('issue_date', False)
        end_on = vals.get('expired_at', False)
        if start_on and end_on:
            self._validate_current_date(date=end_on, limit=start_on, message='fecha inicial')
        bail = super(Bail, self).create(vals)
        return bail
