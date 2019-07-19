import io

import pdfrw
from reportlab.pdfgen import canvas


def run():
    canvas_data = get_overlay_canvas()
    form = merge(canvas_data, template_path='./media/pdf-templates/LHP_Employee_Health_Application_2019.pdf')
    save(form, filename='merged.pdf')


def get_overlay_canvas() -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.drawString(x=33, y=550, text='Willis')
    pdf.drawString(x=148, y=550, text='John')
    pdf.save()
    data.seek(0)
    return data


def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())

data_dict = {
   'business_name_1': 'Bostata',
   'customer_name': 'company.io',
   'customer_email': 'joe@company.io',
   'invoice_number': '102394',
   'send_date': '2018-02-13',
   'due_date': '2018-03-13',
   'note_contents': 'Thank you for your business, Joe',
   'item_1': 'Data consulting services',
   'item_1_quantity': '10 hours',
   'item_1_price': '$200/hr',
   'item_1_amount': '$2000',
   'subtotal': '$2000',
   'tax': '0',
   'discounts': '0',
   'total': '$2000',
   'business_name_2': 'Bostata LLC',
   'business_email_address': 'hi@bostata.com',
   'business_phone_number': '(617) 930-4294'
}