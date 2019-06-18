# -*- coding: utf-8 -*-
from odoo import models, fields, api, osv, tools
from openerp.tools.translate import _
from odoo.exceptions import UserError, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)


class EndorsementReason(models.Model):
    _name = 'psdc_project.endorsement_reason'
    _rec_name = 'reason'
    reason = fields.Char(
        string='Motivo',
        required=True)


class Endorsement(models.Model):
    _name = 'psdc_project.endorsement'
    _rec_name = 'number'
    number = fields.Char(
        string='N de Endozo',
        required=True)
    endorsement_reason_id = fields.Many2one(
        'psdc_project.endorsement_reason',
        string='Motivo del Endozo',
        required=True)
    bail_id = fields.Many2one(
        'psdc_project.bail',
        string='Fianza')
    observation = fields.Text(
        string='Observación',
        required=False)
