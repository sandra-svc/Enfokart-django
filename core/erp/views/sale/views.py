from argparse import Action
from audioop import reverse
from decimal import Decimal
import json
import locale
from babel.numbers import format_currency
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404
import os
import pdb
from urllib import request


from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from weasyprint import HTML, CSS
from .utils import DecimalEncoder




from core.erp.forms import SaleForm, ClientForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale, Product, DetSale, Client, Payment, ProductPhase


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for sale in Sale.objects.all()[0:15]:
                    sale_data = sale.toJSON()
                    sale_data['saldo_pendiente'] = sale.saldo_pendiente()  # Calcula el saldo pendiente para cada venta
                    data.append(sale_data)
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_details_pays':
                if 'id' in request.POST:
                    sale_id = int(request.POST['id'])
                    data = []
                    for payment in Payment.objects.filter(sale_id=sale_id).exclude(amount=0):
                        data.append(payment.toJSON())
                else:
                    data['error'] = 'ID de venta no proporcionado en la solicitud'
            
        except Exception as e:
             import traceback
             traceback.print_exc()
             data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter()
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.date_end = vents['date_end']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                                    
                    for payment_data in vents['payments']:
                        payment = Payment()
                        payment.amount = float(payment_data['amount'])
                        payment.payment_date = payment_data['payment_date']
                        payment.payment_method = payment_data['payment_method']
                        payment.payment_form = payment_data['payment_form']
                        payment.sale = sale
                        payment.save()
                        
                       
                 
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        product = Product.objects.get(id=i['id'])
                        if  product.is_service == False :
                            det.prod.stock -= det.cant
                            det.prod.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        return context


class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['cli'].queryset = Client.objects.filter(id=instance.cli.id)
        return form
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter()
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.date_end = vents['date_end']
                    sale.cli_id = vents['cli']
                    sale.subtotal = str(vents['subtotal'])
                    sale.iva = str(vents['iva'])
                    sale.total = str(vents['total'])
                    sale.save()
                    # Obtener los detalles actuales de la venta
                    current_details = {det.prod_id: det for det in sale.detsale_set.all()}

                    print("Detalles de venta actuales:", current_details)
                    
                    
                    for payment_data in vents['payments']:
                        payment = Payment()
                        payment.amount = float(payment_data['amount'])
                        payment.payment_date = payment_data['payment_date']
                        payment.payment_method = payment_data['payment_method']
                        payment.payment_form = payment_data['payment_form']
                        payment.sale = sale
                        payment.save()
                        
                       
                        

                    for i in vents['products']:
                        det = current_details.get(i['id'])

                        if det:
                            # Producto ya existe en el detalle de la venta, actualizar cantidad
                            old_quantity = det.cant
                            new_quantity = int(i['cant'])
                            quantity_difference = new_quantity - old_quantity

                            det.cant = new_quantity
                            det.price = str(i['pvp'])
                            det.subtotal = str(i['subtotal'])
                            det.save()

                            # Ajustar el stock según la diferencia de cantidad
                            det.prod.stock -= quantity_difference
                            det.prod.save()
                            print(f"Producto: {det.prod.name}, Cantidad anterior: {old_quantity}, Nueva cantidad: {new_quantity}, Diferencia: {quantity_difference}, Nuevo stock: {det.prod.stock}")

                        else:
                            # Producto nuevo, crear un nuevo detalle
                            det = DetSale()
                            det.sale_id = sale.id
                            det.prod_id = i['id']
                            det.cant = int(i['cant'])
                            det.price = str(i['pvp'])
                            det.subtotal = str(i['subtotal'])
                            det.save()

                            # Ajustar el stock del nuevo producto
                            det.prod.stock -= det.cant
                            det.prod.save()
                            print(f"Producto nuevo: {det.prod.name}, Cantidad: {det.cant}, Nuevo stock: {det.prod.stock}")

                    # Manejar productos eliminados
                    deleted_products = request.POST.getlist('deleted_products[]')
                    for prod_id in deleted_products:
                        prod_id = int(prod_id)
                        if prod_id in current_details:
                            det = current_details[prod_id]
                            # Devolver la cantidad eliminada al inventario
                            det.prod.stock += det.cant
                            det.prod.save()
                            print(f"Producto eliminado: {det.prod.name}, Cantidad devuelta: {det.cant}, Nuevo stock: {det.prod.stock}")
                            det.delete()
                data = {'id': sale.id}

            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(),cls=DecimalEncoder)
        context['frmClient'] = ClientForm()
        return context


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context

class SaleInvoicePdfView(View):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ 1. Obtener la venta o devolver un error 404 si no existe
            sale = get_object_or_404(Sale, pk=self.kwargs['pk'])

            # ✅ 2. Calcular valores
            total_pago = sale.total_pago()
            saldo_pendiente = sale.saldo_pendiente()

            # 🔥 CORRECCIÓN: Eliminar `C.UTF-8` y usar directamente `es_CO`
            saldo_pendiente = format_currency(saldo_pendiente, 'USD', locale='es_CO').replace("US$", "$")

            # ✅ 3. Obtener la plantilla y definir el contexto
            template = get_template('sale/invoice.html')
            context = {
                'sale': sale,
                'total_pago': total_pago,
                'saldo_pendiente': saldo_pendiente,
            }

            # ✅ 4. Formatear valores correctamente
            context['sale'].subtotal = format_decimal(sale.subtotal, locale='es_CO')
            context['sale'].iva = format_decimal(sale.iva, locale='es_CO')
            context['sale'].total = format_decimal(sale.total, locale='es_CO')

            # ✅ 5. Renderizar la plantilla con el contexto
            html = template.render(context)

            # ✅ 6. Verificar que el CSS existe antes de usarlo
            css_path = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            stylesheets = [CSS(css_path)] if os.path.exists(css_path) else []

            # ✅ 7. Generar el PDF
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=stylesheets)
            return HttpResponse(pdf, content_type='application/pdf')

        except Http404:
            return HttpResponse("Factura no encontrada", status=404)

        except Exception as e:
            error_message = f"Error interno del servidor: {str(e)}"
            return HttpResponseServerError(error_message)
