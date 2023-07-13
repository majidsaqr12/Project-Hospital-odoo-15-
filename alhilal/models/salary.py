from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AlhilalSalary(models.Model):
    _name = "alhilal.salary"
    _description = "Alhilal Salary for Doctors and Nurses"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'doctor_id'

    doctor_id = fields.Many2one("alhilal.doctor", string="Doctor's name", tracking=True)

    image = fields.Image(string="Image", related="doctor_id.image")

    salary = fields.Integer(string="Salary", related="doctor_id.salary", readonly=True)

    bonus = fields.Integer(string="Bonus", tracking=True)

    total_salary = fields.Integer(string="Total Salary", compute="_compute_total_salary", readonly=True)

    note = fields.Html(string="Note")

    # priority
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')],
                                string="Priority", help='Gives the sequence order')
    # state bar
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'),
                              ('cancel', 'Canceled')], string="State", default="draft", required=True)

    # ( Override on unlink method [ Delete ] )
    def unlink(self):
        for rec in self:
            if rec.state and rec.state != "done" and rec.state != "cancel":
                raise ValidationError(_("You can delete only state in (Done and Cancel)"))
        return super(AlhilalSalary, self).unlink()

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    @api.onchange("doctor_id", "bonus")
    def _compute_total_salary(self):
        for rec in self:
            if rec.doctor_id:
                rec.total_salary = rec.salary + rec.bonus
            else:
                rec.total_salary = 0
