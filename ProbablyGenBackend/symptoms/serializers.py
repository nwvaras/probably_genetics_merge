from rest_framework import serializers

from ml.models import HPOToDisorder, Disorder


class SymptomsQueryInputSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=512)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HPOToDisorderSerializer(serializers.ModelSerializer):

    class Meta:
        model = HPOToDisorder
        fields = ('term', 'freq', 'disorder')


class DisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = ('name',)


class DisorderPercentSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Disorder
        fields = ('id', 'name', 'value')

    def get_value(self, obj):
        return obj.percent

