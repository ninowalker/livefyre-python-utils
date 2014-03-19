Livefyre Python Utility Classes
===============================

Livefyre's official library for common server-side tasks necessary for getting Livefyre apps (comments, reviews, etc.) working on your website.

Works with Python versions: 2.6, 2.7, 3.2, 3.3

Installation
============

    pip install livefyre

Usage
=====

Creating tokens:

**User auth token:**

    network = Livefyre.get_network(network_name, network_key)
    network.build_user_auth_token(user_id, display_name, expires)

**Collection meta token:**

    network = Livefyre.get_network(network_name, network_key)

    site = network.get_site(site_id, site_key)
    site.build_collection_meta_token(title, article_id, url, tags)


To validate a Livefyre token:

    network = Livefyre.get_network(network_name, network_key)
    network.validate_livefyre_token(token)


To send Livefyre a user sync url and then have Livefyre pull user data from that url:

    network = Livefyre.get_network(network_name, network_key)
    
    network.set_user_sync_url('http://thisisa.test.url/{id}/'')
    network.sync_user(system)

        
To retrieve content collection data as a tuple:

    network = Livefyre.get_network(network_name, network_key)
    
    site = network.get_site(site_id, site_key)
    site.get_collection_content(article_id)

License
=======

MIT