from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from payment.models import Payment
from payment.validators import PayValidator
from study.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Payment """

    class Meta:
        model = Payment
        fields = '__all__'
        validators = [PayValidator(field1='paid_course', field2='paid_lesson')]
