import os


env_vars_loaded = os.environ.get('DEBUG', False)

# Fallback for when env variables are not loaded:
if not env_vars_loaded:
    try:
        print('Loading keys from file...')
        current_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        file_path = os.path.join(current_directory, '.env')
        print(file_path)
        with open(file_path, 'r') as f:
            output = f.read()
            output = output.split('\n')

        for var in output:
            if var and not var.startswith('#'):
                k, v = var.split('=', maxsplit=1)
                os.environ.setdefault(k, v)
    except FileNotFoundError:
        print('Environmental variables file not found: {}'.format(file_path))
