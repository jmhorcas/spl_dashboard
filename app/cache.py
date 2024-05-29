import flask_caching


cache = flask_caching.Cache(config={'CACHE_TYPE': 'FileSystemCache',
                                    'CACHE_DIR': '/tmp', 
                                    'CACHE_DEFAULT_TIMEOUT': 3000})  # 50 min