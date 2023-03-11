# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.authentication_request import AuthenticationRequest  # noqa: E501
from swagger_server.models.authentication_token import AuthenticationToken  # noqa: E501
from swagger_server.models.enumerate_offset import EnumerateOffset  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.package import Package  # noqa: E501
from swagger_server.models.package_history_entry import PackageHistoryEntry  # noqa: E501
from swagger_server.models.package_id import PackageID  # noqa: E501
from swagger_server.models.package_metadata import PackageMetadata  # noqa: E501
from swagger_server.models.package_name import PackageName  # noqa: E501
from swagger_server.models.package_query import PackageQuery  # noqa: E501
from swagger_server.models.package_rating import PackageRating  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_auth_token(self):
        """Test case for create_auth_token

        
        """
        body = AuthenticationRequest()
        response = self.client.open(
            '/authenticate',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_by_name_delete(self):
        """Test case for package_by_name_delete

        Delete all versions of this package.
        """
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package/byName/{name}'.format(name=PackageName()),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_by_name_get(self):
        """Test case for package_by_name_get

        
        """
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package/byName/{name}'.format(name=PackageName()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_create(self):
        """Test case for package_create

        
        """
        body = Package()
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_delete(self):
        """Test case for package_delete

        Delete this version of the package.
        """
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package/{id}'.format(id=PackageID()),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_rate(self):
        """Test case for package_rate

        
        """
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package/{id}/rate'.format(id=PackageID()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_retrieve(self):
        """Test case for package_retrieve

        
        """
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package/{id}'.format(id=PackageID()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_update(self):
        """Test case for package_update

        Update this version of the package.
        """
        body = Package()
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/package/{id}'.format(id=PackageID()),
            method='PUT',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_packages_list(self):
        """Test case for packages_list

        Get packages
        """
        body = [PackageQuery()]
        query_string = [('offset', EnumerateOffset())]
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/packages',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registry_reset(self):
        """Test case for registry_reset

        
        """
        headers = [('x_authorization', AuthenticationToken())]
        response = self.client.open(
            '/reset',
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
