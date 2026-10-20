

import logging
from jinja2 import Template


def show(text, templateName, config):
    path = "./templates/"+templateName

    logging.info("render screen from "+path)
    with open(path, 'r') as f:
        output = Template(f.read()).render({ 'text': text, 'config': config })

    print(output)

