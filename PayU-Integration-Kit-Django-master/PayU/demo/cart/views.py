from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, Http404
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse

from payu.forms import PayUForm
from cart.forms import OrderForm

from django.contrib.webdesign.lorem_ipsum import sentence as lorem_ipsum
from uuid import uuid4
from random import randint
import logging

logger = logging.getLogger('django')

def checkout(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            initial = order_form.cleaned_data
            initial.update({'key': settings.PAYU_INFO['merchant_key'],
                            'surl': request.build_absolute_uri(reverse('order.success')),
                            'furl': request.build_absolute_uri(reverse('order.success')),
                            'curl': request.build_absolute_uri(reverse('order.cancel'))})
            # Once you have all the information that you need to submit to payu
            # create a payu_form, validate it and render response using
            # template provided by PayU.
            payu_form = PayUForm(initial)
            if payu_form.is_valid():
                context = {'form': payu_form,
                           'action': "%s_payment" % settings.PAYU_INFO['payment_url']}
                return render(request, 'payu_form.html', context)
            else:
                logger.error('Something went wrong! Looks like initial data\
                        used for payu_form is failing validation')
                return HttpResponse(status=500)
    else:
        initial = {'txnid': uuid4().hex,
                'productinfo': lorem_ipsum(),
                'amount': randint(100, 1000)/100.0}
        order_form = OrderForm(initial=initial)
    context = {'form': order_form}
    return render(request, 'checkout.html', context)
 @csrf_protect
def success(request):
    if request.method == 'POST':
        if not verify_hash(request.POST):
            logger.warning("Response data for order (txnid: %s) has been "
                           "tampered. Confirm payment with PayU." %
                           request.POST.get('txnid'))
            return redirect('order.failure')
        else:
            logger.warning("Payment for order (txnid: %s) succeeded at PayU" %
                           request.POST.get('txnid'))
            return render(request, 'success.html')
    else:
        raise Http404

def failure(request):
    if request.method == 'POST':
        return render(request, 'failure.html')
    else:
        raise Http404

def cancel(request):
    if request.method == 'POST':
        return render(request, 'cancel.html')
    else:
        raise Http404