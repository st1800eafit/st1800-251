# Universidad EAFIT
# Curso Almacenamiento y Recuperación de Información (ST1800 & ST1801)

# LAB  de SPARK

Basado en la experiencia de haber trabajado con los datos de: datasets/sample_data.csv y el notebook: 'hadoop_spark/spark/Data_processing_using_PySpark.ipynb', 
realizar un proceso de:

* carga de datos csv en spark desde un bucket S3 (desde EMR con Notebooks administrados y con el servicio jupyterhub, desde Google Colab y se deja opcionalmente desde boto3)
* borrar y crear algunas columnas
* realizar filtrados de datos por alguna información que le parezca interesante
* realizar alguna agrupación y consulta de datos categorica, por ejemplo número de casos por región o por sexo/genero.
* finalmente salve los resultados en un bucket público en S3
* realice toda la documentación en el mismo notebook.

Los datos los van a obtener de:

* https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data

o en los [datasets](datasets) hay datos ejemplo de covid19 para colombia.

en lab debe ser ejecutable en AWS EMR con los notebooks de EMR y desde Google Colab; y datos en AWS S3 y google drive. El desarrollo lo puede hacer local con Anaconda3 o python y la libreria pyspark instalada. Tambien lo puede hacer con aws boto3.