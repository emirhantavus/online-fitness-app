from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import SubPlan, SubPlanFeature , Payment, UserSubscription
from .serializers import SubPlanFeatureSerializer, SubPlanSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from datetime import timedelta, datetime, timezone as dt_timezone


class SubPlanView(APIView):
      def get(self, request):
            subplans = SubPlan.objects.all()
            response_data = []      
            for subplan in subplans:
                  features = SubPlanFeature.objects.filter(subplan=subplan)
                  feature_serializer = SubPlanFeatureSerializer(features, many=True)
                  subplan_serializer = SubPlanSerializer(subplan)
                  subplan_data = subplan_serializer.data
                  subplan_data['features'] = feature_serializer.data
                  response_data.append(subplan_data)    
            return Response(response_data, status=status.HTTP_200_OK)
    
class SubPlanViewById(APIView):
      def get(self, request , pk):
            subplan = get_object_or_404(SubPlan, pk=pk)
            features = SubPlanFeature.objects.filter(subplan=subplan)
            feature_serializer = SubPlanFeatureSerializer(features, many=True)
            subplan_serializer = SubPlanSerializer(subplan)
            subplan_data = subplan_serializer.data
            subplan_data['features'] = feature_serializer.data
        
            return Response(subplan_data, status=status.HTTP_200_OK)


class PaymentViewSet(ModelViewSet):
      queryset = Payment.objects.all()
      serializer_class = PaymentSerializer
      permission_classes = [IsAuthenticated]
    

class SubPlanPurchaseView(APIView):
      def post(self, request, pk):
            user = request.user
            subplan = get_object_or_404(SubPlan, pk=pk)

            # Ödeme kaydını oluştur
            payment = Payment.objects.create(
                  user=user,
                  amount=subplan.price,
                  status='completed',
                  timestamp=datetime.now(timezone.utc)
            )

            ready_program = ReadyProgram.objects.get(subplan=subplan)

            # Yeni program
            program = TrainerStudentProgram.objects.create(
                  title=ready_program.title,
                  trainer=None,
                  student=user,
                  start_date=datetime.now(timezone.utc),
                  end_date=datetime.now(timezone.utc) + timedelta(days=30)
            )

            # Hazır egzersizler
            ready_exercises = ReadyExercise.objects.filter(program=ready_program)
            for ready_exercise in ready_exercises:
                  exercise = Exercise.objects.create(
                        program=program,
                        title=ready_exercise.title,
                        sets_reps=ready_exercise.sets_reps,
                        intensity=ready_exercise.intensity,
                        tempo=ready_exercise.tempo,
                        rest=ready_exercise.rest,
                        video_url=ready_exercise.video_url,
                        day=ready_exercise.day
                  )
                  for week in range(1, 5):
                        Evolution.objects.create(
                              exercise=exercise,
                              week_number=week,
                              description=''
                        )

            return Response({
                  'payment': payment.id,
                  'program': program.id
            }, status=status.HTTP_201_CREATED)
            
            
class SubscriptionPurchaseView(APIView):
      permission_classes = [IsAuthenticated]

      def post(self, request):
            user = request.user
            subplan_id = request.data.get('subplan_id')

            if not subplan_id:
                  return Response({'error': 'SubPlan ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            subplan = get_object_or_404(SubPlan, id=subplan_id)

            # Mevcut abonelikleri sonlandır
            UserSubscription.objects.filter(user=user, end_date__gte=dj_timezone.now()).update(end_date=dj_timezone.now())

            # Yeni abonelik oluştur
            start_date = dj_timezone.now()
            end_date = start_date + timedelta(days=30)
            user_subscription = UserSubscription.objects.create(
                  user=user,
                  subplan=subplan,
                  start_date=start_date,
                  end_date=end_date
            )

        # Ödeme kaydını oluştur
            payment = Payment.objects.create(
                  user=user,
                  amount=subplan.price,
                  status='completed',
                  timestamp=dj_timezone.now()
            )

        # Hazır program ve egzersizleri ilişkilendir
            ready_program = ReadyProgram.objects.filter(subplan=subplan).first()
            if ready_program:
                  user_program = ready_program.objects.create(user=user, program=ready_program, start_date=start_date, end_date=end_date)
                  exercises = ReadyExercise.objects.filter(program=ready_program)
                  for exercise in exercises:
                        ReadyExercise.objects.create(
                              user_program=user_program,
                              exercise=exercise,
                              sets_reps=exercise.sets_reps,
                              intensity=exercise.intensity,
                              tempo=exercise.tempo,
                              rest=exercise.rest,
                              day=exercise.day
                        )

            formatted_start_date = user_subscription.start_date.strftime('%Y-%m-%d/%H:%M')
            formatted_end_date = user_subscription.end_date.strftime('%Y-%m-%d/%H:%M')
            formatted_timestamp = payment.timestamp.strftime('%Y-%m-%d/%H:%M')

            return Response({
                  'subscription': {
                        'id': user_subscription.id,
                        'subplan': user_subscription.subplan.id,
                        'user': user_subscription.user.id,
                        'start_date': formatted_start_date,
                        'end_date': formatted_end_date
                  },
                  'payment': {
                        'id': payment.id,
                        'user': payment.user.id,
                        'amount': payment.amount,
                        'timestamp': formatted_timestamp,
                        'status': payment.status
                  }
            }, status=status.HTTP_201_CREATED)
            
            
class TrainerSubscriptionView(APIView):
      permission_classes = [IsAuthenticated]

      def post(self, request):
            user = request.user
            trainer_id = request.data.get('trainer_id')

            if not trainer_id:
                  return Response({'error': 'Trainer ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                  trainer = User.objects.get(id=trainer_id, is_trainer=True)
            except User.DoesNotExist:
                  return Response({'error': 'Trainer not found.'}, status=status.HTTP_404_NOT_FOUND)

            if not trainer.monthly_rate:
                  return Response({'error': 'Trainer monthly rate is not set.'}, status=status.HTTP_400_BAD_REQUEST)

            # Mevcut abonelikleri kontrol et
            existing_program = TrainerStudentProgram.objects.filter(trainer=trainer, student=user, end_date__gte=timezone.now()).first()
            if existing_program:
                  return Response({'error': 'You already have an active subscription with this trainer.'}, status=status.HTTP_400_BAD_REQUEST)

            # Yeni abonelik oluştur
            start_date = timezone.now()
            end_date = start_date + timedelta(days=30)
            program = TrainerStudentProgram.objects.create(
                  trainer=trainer,
                  student=user,
                  title=f'{trainer.first_name} {trainer.last_name} - {user.first_name} {user.last_name} Program',
                  start_date=start_date,
                  end_date=end_date
            )

            # Ödeme kaydını oluştur
            payment = Payment.objects.create(
                  user=user,
                  amount=trainer.monthly_rate,
                  status='completed',
                  timestamp=timezone.now()
            )

            formatted_start_date = program.start_date.strftime('%Y-%m-%d/%H:%M')
            formatted_end_date = program.end_date.strftime('%Y-%m-%d/%H:%M')
            formatted_timestamp = payment.timestamp.strftime('%Y-%m-%d/%H:%M')

            return Response({
                  'program': {
                        'id': program.id,
                        'trainer': program.trainer.id,
                        'student': program.student.id,
                        'title': program.title,
                        'start_date': formatted_start_date,
                        'end_date': formatted_end_date
                  },
                  'payment': {
                        'id': payment.id,
                        'user': payment.user.id,
                        'amount': payment.amount,
                        'timestamp': formatted_timestamp,
                        'status': payment.status
                  }
            }, status=status.HTTP_201_CREATED)