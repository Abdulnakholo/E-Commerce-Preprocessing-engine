from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework import views
from .preprocessing import DataProcessor
import pickle, json, jwt
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import parser_classes, renderer_classes
from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework import views
from .preprocessing import DataProcessor
import pickle, json, jwt
from rest_framework.response import Response

class preprocessed(views.APIView):
    def post(self, request):
        if 'file' in request.data:
            try:
                df = pd.read_csv(request.FILES['file'])
            except:
                df = pd.read_excel(request.FILES["file"])
                pass

        data_processor = DataProcessor(df)
        result_df, pickled = data_processor.clean_and_encode()
        # result_df, var_datetime, var_categorical, var_numerical, pickled = data_processor.clean_and_encode()
        print(result_df.head())
        result_df = result_df.head(10)
        result_json = result_df.to_json(orient='records', date_format='iso')
        # return Response(json.loads(result_json))
        return Response('Data preprocessed successfully')  
