import requests

ACCESS_TOKEN = 'ACCESS TOKEN HERE!'

class FBGraphAPI:
  """
  Gestiona las solicitudes al API de Facebook.
  """

  fb_graph_url = 'https://graph.facebook.com'
  version = '11.0'

  def __init__(self, access_token, version=None):
    self.access_token = access_token
    if version:
      self.version = version

  def get_api_url(self):
    return f'{self.fb_graph_url}/v{self.version}/'

  def url_has_params(self, query_string):
    return '?' in query_string

  def get_call_url(self, query_string):
    token_separator = '&' if self.url_has_params(query_string) else '?'
    return f'{self.get_api_url()}{query_string}{token_separator}access_token={self.access_token}'

  def post_call(self, query_string):
    query_url = self.get_call_url(query_string)
    fb_response = requests.post(query_url)
    return fb_response.json()

  def query_call(self, query_string):
    query_url = self.get_call_url(query_string)
    fb_response = requests.get(query_url)
    return fb_response.json()

class FBPageBroker():
  """
  Recupera los comentarios de una fanpage
  """

  def __init__(self, access_token, page_id):
    self.access_token = access_token
    self.page_id = page_id
    self.fb_api_connector = FBGraphAPI(access_token)

  def get_posts(self):
    query_result = self.fb_api_connector.query_call(f'{self.page_id}/posts')
    return query_result.get('data', [])

  def get_post_comments(self, post_id):
    query_result = self.fb_api_connector.query_call(f'{post_id}?fields=comments')
    return query_result.get('comments', {}).get('data', [])

  def __collect_post_comments(self, posts, io_comment_collector):
    for post in posts:
      io_comment_collector.extend(self.get_post_comments(post.get('id')))

  def get_all_post_comments(self):
    posts = self.get_posts()
    comments = []
    self.__collect_post_comments(posts, io_comment_collector=comments)
    return comments

if __name__ == '__main__':
  fb_page_broker = FBPageBroker(access_token=ACCESS_TOKEN, page_id='FAN PAGE ID HERE!')

  comments = fb_page_broker.get_all_post_comments()
  print(comments)
