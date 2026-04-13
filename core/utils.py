from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.conf import settings

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

def send_invoice_email(booking):
    subject = f"Invoice for your eGarage Service - {booking.service.title}"
    message = f"Hi {booking.customer.username}, your payment has been confirmed. Please find your invoice attached."
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [booking.customer.email])
    
    # Generate PDF
    pdf = render_to_pdf('admin/invoice_pdf.html', {'booking': booking})
    if pdf:
        email.attach(f'invoice_{booking.id}.pdf', pdf, 'application/pdf')
        email.send()