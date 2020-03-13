from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from ml.models import HPOToDisorder, Disorder
from symptoms.serializers import SymptomsQueryInputSerializer, DisorderSerializer, DisorderPercentSerializer
from symptoms.terms_utils import MedicalTermProvider
import pickle
filename = 'randomforest_model.sav'
model = pickle.load(open(filename, 'rb'))

# Test data

syntoms = ['HP:0001939', 'HP:0004322', 'HP:0000518', 'HP:0001482', 'HP:0100585', 'HP:0002486', 'HP:0003457',
           'HP:0002671', 'HP:0200034', 'HP:0001601', 'HP:0001608', 'HP:0002093', 'HP:0002205', 'HP:0002564',
           'HP:0000175', 'HP:0100335', 'HP:0000822', 'HP:0001671', 'HP:0001602', 'HP:0001631', 'HP:0003170',
           'HP:0004915', 'HP:0000282', 'HP:0000969', 'HP:0001541', 'HP:0002027', 'HP:0005214', 'HP:0005225',
           'HP:0012027', 'HP:0100665', 'HP:0001025', 'HP:0002579', 'HP:0012034', 'HP:0012211', 'HP:0001945',
           'HP:0004326', 'HP:0000738', 'HP:0012440', 'HP:0100518']

syn_dict= {'HP:0001939': 0, 'HP:0004322': 1, 'HP:0000518': 2, 'HP:0001482': 3, 'HP:0100585': 4, 'HP:0002486': 5,
           'HP:0003457': 6, 'HP:0002671': 7, 'HP:0200034': 8, 'HP:0001601': 9, 'HP:0001608': 10, 'HP:0002093': 11,
           'HP:0002205': 12, 'HP:0002564': 13, 'HP:0000175': 14, 'HP:0100335': 15, 'HP:0000822': 16, 'HP:0001671': 17,
           'HP:0001602': 18, 'HP:0001631': 19, 'HP:0003170': 20, 'HP:0004915': 21, 'HP:0000282': 22, 'HP:0000969': 23,
           'HP:0001541': 24, 'HP:0002027': 25, 'HP:0005214': 26, 'HP:0005225': 27, 'HP:0012027': 28, 'HP:0100665': 29,
           'HP:0001025': 30, 'HP:0002579': 31, 'HP:0012034': 32, 'HP:0012211': 33, 'HP:0001945': 34, 'HP:0004326': 35,
           'HP:0000738': 36, 'HP:0012440': 37, 'HP:0100518': 38}


disorders = [91378, 91385, 293807, 614, 606, 79237, 99967, 99969, 99971, 211, 163, 867, 112, 2808, 158022, 3189, 67041,
             1202, 3188, 2373]


class SymptomsApiView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SymptomsQueryInputSerializer


class QuerySymptomsApiView(SymptomsApiView):


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        provider = MedicalTermProvider()
        query = serializer.validated_data.get('query')

        # Get medical terms queried
        terms = provider.find_medical_terms(query)

        if len(terms) == 0:
            return Response({'terms': terms, 'results': []})

        # Search for all disorders with all those terms (AND operator)
        disorder_ids = HPOToDisorder.objects.filter(term__icontains=terms[0]).values_list('disorder_id', flat=True)
        for term in terms:
            if term == terms[0]:
                continue
            disorder_ids = HPOToDisorder.objects.filter(term__icontains=term, disorder_id__in=disorder_ids).values_list('disorder_id', flat=True)
        disorders = Disorder.objects.filter(id__in=disorder_ids).all()
        serializer = DisorderSerializer(disorders, many=True)
        return Response({'terms': terms, 'results': serializer.data})


class MLSymptomsApiView(SymptomsApiView):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        provider = MedicalTermProvider()
        query = serializer.validated_data.get('query')

        # Get medical terms queried
        terms = provider.find_medical_terms(query)

        if len(terms) == 0:
            return Response({'terms': terms, 'results': []})

        # Search for all disorders with all those terms (AND operator)
        hp_ids=[]
        for term in terms:
            hp_ids.append(HPOToDisorder.objects.filter(term__icontains=term,disorder_id__in=disorders).values_list('id_hp',flat=True)[0])
        l=[0]*len(syntoms)
        for id in hp_ids:
            l[syn_dict[id]] = 1

        # prediction_id = model.predict([l])
        prediction = model.predict_proba([l])[0]
        print('prediction')
        print(prediction)
        pred_disorders = list(Disorder.objects.filter(id__in=disorders))
        for i in range(0,len(prediction)):
            pred_disorders[i].percent = prediction[i]

        serializer = DisorderPercentSerializer(list(filter(lambda  x: x.percent >0,pred_disorders)), many=True)
        return Response({'terms': terms, 'results': serializer.data})
