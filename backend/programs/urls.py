from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    TrainerStudentProgramViewSet,
    ExerciseProgramViewSet,
    EvolutionViewSet,
    TrainerExerciseListView
)

router = DefaultRouter()
router.register(r'programs', TrainerStudentProgramViewSet, basename='program')
router.register(r'exercise-programs', ExerciseProgramViewSet, basename='exercise-program')
router.register(r'evolution', EvolutionViewSet, basename='evolution')

urlpatterns = [
    path('trainer-exercises/', TrainerExerciseListView.as_view(), name='trainer-exercise-list'),
]

urlpatterns += router.urls
