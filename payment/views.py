import json
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import TransactionSerializer
from .models import Transaction
from django.conf import settings
import razorpay
# Create your views here.

class TransactionCreateAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    
    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        amount = float(request.data.get('amount'))

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEYID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Create a Razorpay order
            razorpay_order = client.order.create({
                'amount': int(amount * 100),  # Razorpay expects amount in paisa
                'currency': 'INR',
                'payment_capture': '1',
            })

            # Extract Razorpay order ID from the response
            razorpay_order_id = razorpay_order['id']
            transaction = Transaction.objects.create(sender=sender, reciever=receiver, amount=amount, transacrtion_id=razorpay_order_id)
            serializer = self.serializer_class(transaction)
            data = {
                "payment": razorpay_order,
                "order": serializer.data
            }

            # Return Razorpay order ID to the frontend
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Handle errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class HandlePaymentSuccessAPIView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def update(self, request, *args, **kwargs):
        res = json.loads(request.data["response"])

        ord_id = res.get('razorpay_order_id')
        raz_pay_id = res.get('razorpay_payment_id')
        raz_signature = res.get('razorpay_signature')
        print(raz_signature)
        transaction = Transaction.objects.get(transacrtion_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        client = razorpay.Client(auth=(settings.RAZORPAY_KEYID, settings.RAZORPAY_KEY_SECRET))

        try:
            check = client.utility.verify_payment_signature(data)

            # if check is not None:
            #     return Response({'error': 'Signature verification failed'}, status=status.HTTP_400_BAD_REQUEST)

            transaction.is_completed = True
            transaction.save()

            res_data = {
                'message': 'Payment successfully received!'
            }

            return Response(res_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    