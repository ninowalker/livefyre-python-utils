import base64, jwt, re, requests, sys, time

try:
    import simplejson as json
except ImportError:
    import json
    

class Network(object):
    DEFAULT_USER = 'system'
    DEFAULT_EXPIRES = 86400
    
    def __init__(self, network_name, network_key):
        self.network_name = network_name
        self.network_key = network_key
    
    
    def set_user_sync_url(self, url_template):
        assert '{id}' in url_template, 'url_template should have {id}.'
        
        url = 'http://{0!s}/'.format(self.network_name)
        data = {'actor_token' : self.build_lf_token(), 'pull_profile_url' : url_template}
        headers = {'Content-type': 'application/json'}
        
        request = requests.post(url=url, data=data, headers=headers)
        return request.status_code is 204
        
        
    def sync_user(self, user_id):
        url = 'http://{0!s}/api/v3_0/user/{1!s}/refresh'.format(self.network_name, user_id)
        data = {'lftoken' : self.build_lf_token()}
        headers = {'Content-type': 'application/json'}
        
        request = requests.post(url=url, data=data, headers=headers)
        return request.status_code is 200
    
    
    def build_lf_token(self):
        return self.build_user_auth_token(self.DEFAULT_USER, self.DEFAULT_USER, self.DEFAULT_EXPIRES)
    
    def build_user_auth_token(self, user_id, display_name, expires):
        assert user_id.isalnum(), 'user_id should only contain alphanumeric characters'

        return jwt.encode({
                'domain': self.network_name,
                'user_id': user_id,
                'display_name': display_name,
                'expires': int(time.time()) + expires},
            self.network_key)
    
    
    def validate_livefyre_token(self, lf_token):
        token_attr = jwt.decode(lf_token, self.network_key)
        return (token_attr['domain'] == self.network_name
            and token_attr['user_id'] == self.DEFAULT_USER
            and token_attr['expires'] >= int(time.time()))
        
    
    def get_site(self, site_id, site_key):
        return Site(self.network_name, site_id, site_key)


class Site(object):
    def __init__(self, network_name, site_id, site_key):
        self.network_name = network_name
        self.site_id = site_id
        self.site_key = site_key
    
    
    def build_collection_meta_token(self, title, article_id, url, tags, stream=''):
        assert re.match(r'^http[s]{0,1}://[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*$', url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        return jwt.encode({
                'title': title,
                'url': url,
                'tags': tags,
                'articleId': article_id,
                'type': stream
                },
            self.site_key)
    
    
    def get_collection_content(self, article_id):
        if sys.version_info >= (3, 0):
            article_bytes = bytes(str(article_id), 'utf-8')
        else:
            article_bytes = bytes(str(article_id))
        encoded_article_id = base64.b64encode(article_bytes).decode('utf-8')
        url = 'http://bootstrap.{0!s}/bs3/{0!s}/{1!s}/{2!s}/init'.format(self.network_name, self.site_id, encoded_article_id)
        
        response = requests.get(url=url)
        if response.status_code == 200:
            return json.loads(response.content)
        return ''