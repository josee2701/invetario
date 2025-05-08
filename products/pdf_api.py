# products/pdf_api.py

"""
Vista y serializador para generar un PDF con los datos de Stock y enviarlo por correo.
"""
from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from rest_framework import response, serializers, status, views

from .models import Stock
from .serializers import StockSerializer


class StockPDFRequestSerializer(serializers.Serializer):
    """
    Recibe el correo de destino y el asunto para el envío del PDF.
    """
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)


class StockPDFView(views.APIView):
    """
    POST /api/stocks/pdf/

    Request:
    {
        "email": "destinatario@dominio.com",
        "subject": "Asunto del correo"
    }

    Response:
        200 OK con mensaje de éxito o 400 en caso de datos inválidos.
    """
    def post(self, request):
        # Validar datos de entrada
        serializer = StockPDFRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_destino = serializer.validated_data['email']
        asunto = serializer.validated_data['subject']

        # Serializar datos de stock
        stocks = Stock.objects.all()
        stock_data = StockSerializer(stocks, many=True, context={'request': request}).data

        # Generar PDF en memoria
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        y = 800
        for stock in stock_data:
            linea = (
                f"ID: {stock['id']} | "
                f"Producto: {stock['product_detail']['cod']} - {stock['product_detail']['name']} | "
                f"Cantidad: {stock['quantity']} | Fecha: {stock['date']}"
            )
            pdf.drawString(40, y, linea)
            y -= 20
            if y < 40:
                pdf.showPage()
                y = 800
        pdf.save()
        buffer.seek(0)

        # Enviar correo con el PDF adjunto desde la cuenta configurada en settings
        email_msg = EmailMessage(
            subject=asunto,
            body='Adjunto PDF con información de stock.',
            from_email=settings.EMAIL_HOST_USER,
            to=[email_destino]
        )
        email_msg.attach('stocks.pdf', buffer.read(), 'application/pdf')
        email_msg.send(fail_silently=False)

        return response.Response(
            {'detail': 'Correo enviado correctamente.'},
            status=status.HTTP_200_OK
        )

# URLs (en tu urls.py):
# from products.pdf_api import StockPDFView
# urlpatterns += [
#     path('api/stocks/pdf/', StockPDFView.as_view(), name='stocks-pdf'),
# ]
