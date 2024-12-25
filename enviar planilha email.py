import pandas as pd
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def convert_excel_to_pdf(excel_file, pdf_file):
    # Ler o arquivo Excel
    df = pd.read_excel(excel_file)

    # Configurar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adicionar o conteúdo do DataFrame ao PDF
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    spacing = 1.3

    for i in range(len(df)):
        for datum in df.iloc[i]:
            pdf.cell(col_width, row_height * spacing, str(datum), border=1)
        pdf.ln(row_height * spacing)

    # Salvar o PDF
    pdf.output(pdf_file)


def send_email(subject, body, to_email, from_email, from_password, attachment_path):
    # Configurar a mensagem do email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Adicionar o corpo do email
    msg.attach(MIMEText(body, 'plain'))

    # Adicionar o anexo
    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
    msg.attach(part)

    # Configurar o servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)

    # Enviar o email
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


if __name__ == '__main__':
    # Caminhos dos arquivos
    excel_file = 'caminho_para_sua_planilha.xlsx'
    pdf_file = 'planilha_convertida.pdf'

    # Converter Excel para PDF
    convert_excel_to_pdf(excel_file, pdf_file)

    # Configurações do email
    subject = "Sua Planilha Convertida"
    body = "Segue em anexo a planilha convertida para PDF."
    to_email = "destinatario@example.com"
    from_email = "seuemail@gmail.com"
    from_password = "suasenha"

    # Enviar o email com o PDF anexado
    send_email(subject, body, to_email, from_email, from_password, pdf_file)
