from datetime import date
from dateutil import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AlhilalPatient(models.Model):
    _name = 'alhilal.patient'
    _description = 'Alhilal Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Personal info
    name = fields.Char(string="Name", tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age", inverse='_inverse_compute_age', search="_search_age",
                         tracking=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    phone = fields.Char(string="Phone", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    social_security_number = fields.Integer('Social security number')
    image = fields.Image(string="Image")
    patient_id = fields.Char(readonly=True)
    charge_dr = fields.Many2one('alhilal.doctor', string='Charge dr')
    tags_ids = fields.Many2many('patient.tag', string="Tags")

    parent = fields.Char(string="Parent", tracking=True)
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital status",
                                      tracking=True)
    partner_name = fields.Char(string="Partner Name")

    # vital signs
    blood_pressure = fields.Integer(string='Blood pressure')
    heart_rate = fields.Integer(string='Heart rate')
    respiratory_rate = fields.Integer(string='Respiratory rate')

    # Notebooks
    medical_history = fields.Html()
    diagnosis_and_treatment_plan = fields.Html()
    progress_notes = fields.Html()
    nursing_notes = fields.Html()
    physician_orders = fields.Html()
    discharge_summary = fields.Html()
    insurance_info = fields.Html()

    appointment_ids = fields.One2many('alhilal.appointment', 'patient_id', string="Appointment")

    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['alhilal.appointment'].search_count([('patient_id', '=', rec.id)])

    # ( Method To Check on Fields )
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date of birth is not acceptable"))

    @api.constrains('name')
    def _check_name(self):
        if self.name and self.name is None:
            raise ValidationError(_("Name is Missed"))

    # Override on Create method [ create ]
    @api.model
    def create(self, vals_list):
        # create sequence
        vals_list['patient_id'] = self.env['ir.sequence'].next_by_code('alhilal.patient')
        return super(AlhilalPatient, self).create(vals_list)

    # Override on write method [ Edit ]
    def write(self, vals):
        if not self.patient_id and vals.get('patient_id'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('alhilal.patient')
        return super(AlhilalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]
