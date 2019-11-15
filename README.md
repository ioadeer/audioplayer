# Corpus based concatenative synth 
## Forma de uso:

En el directiorio tipear:
<code>python test.py </code>

Descargar carpeta de archivos analizados [acá](https://www.dropbox.com/sh/97d251paw47c79p/AABjbe5LjjPc6AhFiqJgI1psa?dl=0).

Navegar al directorio analyzed y escoger un directorio (v-gr "aphex twin"). Una vez en el directorio sellecionar un archivo wav.

Una vez cargado los archivos de análisis, de la lista Features seleccionar los descriptores que se desee(para deseleccionarlos hacer click en el nombre del descriptor en esa lista). Gran Size determina qué archivo se carga y va a determinar qué tamaño de grano se va  utilizar en la reproducción.

Para utilizar los descriptores seleccionados para las reproducción y/o realizar PCA, primero hay que hacer click en Filter Features con descriptores presentes en la lista de Selected Features. Hay features que no sirven para hacer PCA, como por ejemplo loudness\_ebu128 y loudness\_ebu128.1. Para hacer PCA luego hay que hacer click en Perform PCA.

En la pestaña Play la lista, de drop down debajo de Sort by: debe haberse poblado con descriptores. Seleccionar el que se quiera escuchar y luego hacer click en el botón rearrange para procesar el audio y en el botón normal para volverlo al orden inicial. Debe estar seleccionado play para que se reproduzca. El slider horizontal sirve para seleccionar un punto en el audio, pero su posicion no se actualiza. Ascending y Descending no está implementado todavía.
