# Copyright 2020 The FedLearner Authors. All Rights Reserved.
#
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

# coding: utf-8

import os
import logging
import kubernetes
from kubernetes.client.rest import ApiException
from fedlearner import settings


class K8sClient(object):
    def __init__(self,
                 token_path=settings.K8S_TOKEN_PATH,
                 ca_path=settings.K8S_CAS_PATH,
                 service_host=settings.KUBERNETES_SERVICE_HOST,
                 service_port=settings.KUBERNETES_SERVICE_PORT):
        os.environ['KUBERNETES_SERVICE_HOST'] = service_host
        os.environ['KUBERNETES_SERVICE_PORT'] = service_port
        loader = kubernetes.config.incluster_config.InClusterConfigLoader(
            token_path, ca_path)
        loader.load_and_set()
        # Configure API key authorization: BearerToken
        configuration = kubernetes.client.Configuration()
        # configuration.api_key['authorization'] = 'YOUR_API_KEY'
        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['authorization'] = 'bearer'
        self._api = kubernetes.client.CustomObjectsApi(
            kubernetes.client.ApiClient(configuration))

    @property
    def api(self):
        return self._api

    def create_crd(self, yaml_body, namespace='default'):
        return self._api.create_namespaced_custom_object(
            settings.FL_CRD_GROUP, settings.FL_CRD_VERSION, namespace,
            settings.FL_CRD_PLURAL, yaml_body)

    def delete_crd(self, name, namespace='default'):
        body = kubernetes.client.V1DeleteOptions()  # V1DeleteOptions |
        try:
            return self._api.delete_namespaced_custom_object(
                settings.FL_CRD_GROUP, settings.FL_CRD_VERSION, namespace,
                settings.FL_CRD_PLURAL, name, body)
        except ApiException as e:
            logging.error(
                "Exception when calling "
                "CustomObjectsApi->delete_namespaced_custom_object: %s\n", e)
        return None

    def get_crd_object(self, name, namespace='default'):
        try:
            return self._api.get_namespaced_custom_object(
                settings.FL_CRD_GROUP, settings.FL_CRD_VERSION, namespace,
                settings.FL_CRD_PLURAL, name)
        except ApiException as e:
            logging.error(
                "Exception when calling"
                " CustomObjectsApi->get_namespaced_custom_object: %s\n", e)
        return None

    def get_crd_object_status(self, name, namespace='default'):
        try:
            return self._api.get_namespaced_custom_object_status(
                settings.FL_CRD_GROUP, settings.FL_CRD_VERSION, namespace,
                settings.FL_CRD_PLURAL, name)
        except ApiException as e:
            logging.error(
                "Exception when calling"
                " CustomObjectsApi->get_namespaced_custom_object_status: %s\n",
                e)
        return None

    def list_crd_object(self, namespace='default'):
        try:
            return self._api.list_namespaced_custom_object(
                settings.FL_CRD_GROUP, settings.FL_CRD_VERSION, namespace,
                settings.FL_CRD_PLURAL)
        except ApiException as e:
            logging.error(
                "Exception when calling "
                "CustomObjectsApi->list_namespaced_custom_object: %s\n", e)
        return None
