from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AlhilalAppointment(models.Model):
    _name = 'alhilal.appointment'
    _description = 'Alhilal Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "patient_id"

    seq = fields.Char(readonly=True)
    # value is name of patient
    patient_id = fields.Many2one('alhilal.patient', string="Patient", tracking=True, ondelete="cascade")  # default
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", related='patient_id.gender')
    image = fields.Image(string="Image", related="patient_id.image")
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    prescription = fields.Html(string="Prescription")

    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')],
                                string="Priority", help='Gives the sequence order')

    doctor_id = fields.Many2one('res.users', string="Created By")

    pharmacy_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")

    # state bar
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'),
                              ('cancel', 'Canceled')], string="State", default="draft", required=True)

    patient_ids = fields.Many2one('alhilal.patient', string="Patient")

    hide_column = fields.Boolean(string="Hide column price")

    @api.model
    def create(self, vals_list):
        # create sequence
        vals_list['seq'] = self.env['ir.sequence'].next_by_code('alhilal.appointment')
        return super(AlhilalAppointment, self).create(vals_list)

    # ( Override on unlink method [ Delete ] )
    def unlink(self):
        for rec in self:
            if rec.state and rec.state != "done" and rec.state != "cancel":
                raise ValidationError(_("You can delete only state in (Done and Cancel)"))
        return super(AlhilalAppointment, self).unlink()

    def action_in_consultation(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = "in_consultation"
            else:
                raise ValidationError(_("This state executed only in case draft"))

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def action_draft(self):
        for rec in self:
            rec.state = "draft"


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(string="Price", related="product_id.list_price")
    qyt = fields.Integer(string="Quantity", default=1)

    appointment_id = fields.Many2one('alhilal.appointment', string="Appointment")
