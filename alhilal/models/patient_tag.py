from odoo import fields, models, api, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string="Name")
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    sequence = fields.Integer(string="Sequence")

    # Override on method Copy [ Duplicated ]
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique (name)', 'Name must be unique'),
        ('check_sequence', 'check (sequence > 0)', 'sequence must be positive number')
    ]
