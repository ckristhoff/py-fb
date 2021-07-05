from datetime import datetime as DateTime
import requests

# ACCESS_TOKEN = 'ACCESS TOKEN HERE!'
ACCESS_TOKEN = 'ACCESS TOKEN HERE!'

def datetime_to_unix(datetime):
  """Retorna una cadena de timestamp UNIX a partir de un objeto de fecha y hora."""
  return datetime.strftime('%s')

class FBGraphAPI:
  """Establece la comunicación al API de Facebook."""

  graph_api_url = 'https://graph.facebook.com'
  version = '11.0'

  def __init__(self, access_token, version=None):
    self.access_token = access_token
    if version:
      self.version = version

  def get_api_url(self):
    """Retorna la URL base del API."""
    return f'{self.graph_api_url}/v{self.version}/'

  def url_has_params(self, query_string):
    """Retorna True si la cadena de consulta ya contiene parámetros, Falso si aún no."""
    return '?' in query_string

  def get_calling_url(self, query_string):
    """Retorna la URL completa de consulta (URL base + consulta)."""
    token_separator = '&' if self.url_has_params(query_string) else '?'
    return f'{self.get_api_url()}{query_string}{token_separator}access_token={self.access_token}'

  def query(self, query_string):
    """Retorna un diccionario con el resultado de una consulta al API."""
    url = self.get_calling_url(query_string)
    fb_response = requests.get(url)
    return fb_response.json()

class FBFanPageManager():
  """Ejecuta las operaciones de consulta a un Fan Page de Facebook."""

  def __init__(self, access_token, page_id):
    self.access_token = access_token
    self.page_id = page_id
    self.fb_graph_api = FBGraphAPI(access_token)

  def __serialize_params(self, params_dict):
    """Retorna los parámetros serializados para ser usados en una URL."""
    return ''.join([f'{param_name}={params_dict.get(param_name)}&' for param_name in params_dict.keys()])

  def get_posts(self, **kwargs):
    """Retorna el listado de publicaciones de la Fan Page."""
    params = self.__serialize_params(kwargs)
    query_result = self.fb_graph_api.query(f'{self.page_id}/posts?{params}')
    return query_result.get('data', [])

  def get_post_comments(self, post_id, **kwargs):
    """Retorna el listado de comentarios de una publicación."""
    params = self.__serialize_params(kwargs)
    query_result = self.fb_graph_api.query(f'{post_id}?fields=comments&{params}')
    return  query_result.get('comments', {}).get('data', [])

  def __collect_post_comments(self, posts):
    """
    Consulta y retorna la lista de comentarios de la lista de publicaciones dada;
    la consulta se realiza de forma paralela para mayor rendimiento.
    """
    import multiprocessing
    with multiprocessing.Pool(multiprocessing.cpu_count()) as process_pool:
      comments = process_pool.map(self.get_post_comments, [post.get('id') for post in posts])
    return [_comment for _comments in comments for _comment in _comments]

  def get_all_post_comments(self, **kwargs):
    """Retorna el listado de comentarios de todas las publicaciones de la Fan Page."""
    posts = self.get_posts(**kwargs)
    return self.__collect_post_comments(posts)

if __name__ == '__main__':
  # ejemplo de uso
  fb_fanpage_manager = FBFanPageManager(access_token=ACCESS_TOKEN, page_id='FAN PAGE ID HERE!')
  since_filter = datetime_to_unix(DateTime(2013, 4, 1, 15, 55, 54))
  until_filter = datetime_to_unix(DateTime(2021, 7, 3, 14, 55, 53))
  comments = fb_fanpage_manager.get_all_post_comments(since=since_filter, until=until_filter)
  print(comments)
