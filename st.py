# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

logger = logging.getLogger('clusterdock.{}'.format(__name__))

EXTRA_LIB_IMAGE_NAME_TEMPLATE = '{}/{}/transformer:{}'
IMAGE_NAME_TEMPLATE = '{}/{}/transformer:{}'

EXTRA_LIBS_SUPPORTED = ['jdbc']
ST_PORT = 19630 # inline to ST build
ST_USER = 'sdc' # TODO: change from SDC convention to ST convention when ST build changes
ST_USER_ID = 20169 # inline to ST build


class Transformer:
    def __init__(self, version, namespace, registry):
        self.namespace = namespace
        self.registry = registry
        self.version = version

        self.image_name = IMAGE_NAME_TEMPLATE.format(self.registry, self.namespace, self.version)
        self.extra_lib_images = [EXTRA_LIB_IMAGE_NAME_TEMPLATE.format(self.registry, self.namespace, image)
                                 for image in EXTRA_LIBS_SUPPORTED]
        # TODO: convention to change from SDC to ST when ST build is ready
        self.home_dir = '/opt/streamsets-transformer-{}'.format(self.version)
        self.environment = {
            'SDC_RESOURCES': '/resources/st',
            'STREAMSETS_LIBRARIES_EXTRA_DIR': '/opt/streamsets-libs-extras',
            'SDC_DATA': '/data/st',
            'SDC_DIST': self.home_dir,
            'SDC_HOME': self.home_dir,
            'USER_LIBRARIES_DIR': '/opt/streamsets-transformer-user-libs',
            'SDC_CONF': '/etc/st',
            'SDC_LOG': '/logs/st',
            'JAVA_HOME': '/opt/java/openjdk', # inline to what ST docker build uses
            'SPARK_HOME': '/opt/cloudera/parcels/CDH/lib/spark'
        }

    def commands_for_add_user(self):
        return ['groupadd -r -g {} {}'.format(ST_USER_ID, ST_USER),
                'useradd -r -u {} -g {} {}'.format(ST_USER_ID, ST_USER, ST_USER)]

    def command_for_execute(self):
        return 'exec {}/bin/streamsets transformer -exec'.format(self.home_dir)
