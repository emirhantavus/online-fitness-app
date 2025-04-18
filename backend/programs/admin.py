from django.contrib import admin
from .models import (
    TrainerStudentProgram, Exercise, Evolution,
    ReadyProgram, ReadyExercise
)

@admin.register(TrainerStudentProgram)
class TrainerStudentProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'student', 'start_date', 'end_date')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'sets_reps', 'intensity', 'day')

@admin.register(Evolution)
class EvolutionAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'week_number', 'description')

@admin.register(ReadyProgram)
class ReadyProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'subplan')

@admin.register(ReadyExercise)
class ReadyExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'sets_reps', 'day')
