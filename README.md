# PY-FB

Prueba de concepto para recuperar los comentarios de una fanpage de Facebook usando su API de desarrolladores.

## Requerimientos

1. Crear app en [Facebook Developers](https://developers.facebook.com/)
2. Obtener un token de acceso siguiendo las siguientes [instrucciones](https://developers.facebook.com/docs/marketing-apis/overview/authentication/?locale=es_LA)
3. Obtener el ID de la fanpage siguiendo las siguientes [instrucciones](https://www.facebook.com/help/1503421039731588)
4. Configurar el token de acceso en el código fuente
```python
ACCESS_TOKEN = 'ACCESS TOKEN HERE!'
```
5. Suministrar el ID de la fan page al constructor de la clase `FBPageBroker`
```python
fb_page_broker = FBPageBroker(access_token=ACCESS_TOKEN, page_id='FAN PAGE ID HERE!')
```
6. Ejecutar.
