# swagger_client.DefaultApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_auth_token**](DefaultApi.md#create_auth_token) | **PUT** /authenticate | 
[**package_by_name_delete**](DefaultApi.md#package_by_name_delete) | **DELETE** /package/byName/{name} | Delete all versions of this package.
[**package_by_name_get**](DefaultApi.md#package_by_name_get) | **GET** /package/byName/{name} | 
[**package_create**](DefaultApi.md#package_create) | **POST** /package | 
[**package_delete**](DefaultApi.md#package_delete) | **DELETE** /package/{id} | Delete this version of the package.
[**package_rate**](DefaultApi.md#package_rate) | **GET** /package/{id}/rate | 
[**package_retrieve**](DefaultApi.md#package_retrieve) | **GET** /package/{id} | 
[**package_update**](DefaultApi.md#package_update) | **PUT** /package/{id} | Update this version of the package.
[**packages_list**](DefaultApi.md#packages_list) | **POST** /packages | Get packages
[**registry_reset**](DefaultApi.md#registry_reset) | **DELETE** /reset | 

# **create_auth_token**
> AuthenticationToken create_auth_token(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.AuthenticationRequest() # AuthenticationRequest | 

try:
    api_response = api_instance.create_auth_token(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->create_auth_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuthenticationRequest**](AuthenticationRequest.md)|  | 

### Return type

[**AuthenticationToken**](AuthenticationToken.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_by_name_delete**
> package_by_name_delete(name, x_authorization=x_authorization)

Delete all versions of this package.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
name = swagger_client.PackageName() # PackageName | 
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    # Delete all versions of this package.
    api_instance.package_by_name_delete(name, x_authorization=x_authorization)
except ApiException as e:
    print("Exception when calling DefaultApi->package_by_name_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | [**PackageName**](.md)|  | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_by_name_get**
> list[PackageHistoryEntry] package_by_name_get(name, x_authorization=x_authorization)



Return the history of this package (all versions).

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
name = swagger_client.PackageName() # PackageName | 
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    api_response = api_instance.package_by_name_get(name, x_authorization=x_authorization)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->package_by_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | [**PackageName**](.md)|  | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

[**list[PackageHistoryEntry]**](PackageHistoryEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_create**
> PackageMetadata package_create(body, x_authorization)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.Package() # Package | 
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken | 

try:
    api_response = api_instance.package_create(body, x_authorization)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->package_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Package**](Package.md)|  | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | 

### Return type

[**PackageMetadata**](PackageMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_delete**
> package_delete(id, x_authorization=x_authorization)

Delete this version of the package.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
id = swagger_client.PackageID() # PackageID | Package ID
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    # Delete this version of the package.
    api_instance.package_delete(id, x_authorization=x_authorization)
except ApiException as e:
    print("Exception when calling DefaultApi->package_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**PackageID**](.md)| Package ID | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_rate**
> PackageRating package_rate(id, x_authorization=x_authorization)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
id = swagger_client.PackageID() # PackageID | 
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    api_response = api_instance.package_rate(id, x_authorization=x_authorization)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->package_rate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**PackageID**](.md)|  | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

[**PackageRating**](PackageRating.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_retrieve**
> Package package_retrieve(id, x_authorization=x_authorization)



Return this package.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
id = swagger_client.PackageID() # PackageID | ID of package to fetch
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    api_response = api_instance.package_retrieve(id, x_authorization=x_authorization)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->package_retrieve: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**PackageID**](.md)| ID of package to fetch | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

[**Package**](Package.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **package_update**
> package_update(body, id, x_authorization=x_authorization)

Update this version of the package.

The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.Package() # Package | 
id = swagger_client.PackageID() # PackageID | 
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    # Update this version of the package.
    api_instance.package_update(body, id, x_authorization=x_authorization)
except ApiException as e:
    print("Exception when calling DefaultApi->package_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Package**](Package.md)|  | 
 **id** | [**PackageID**](.md)|  | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **packages_list**
> list[PackageMetadata] packages_list(body, x_authorization=x_authorization, offset=offset)

Get packages

Get any packages fitting the query.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = [swagger_client.PackageQuery()] # list[PackageQuery] | 
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)
offset = swagger_client.EnumerateOffset() # EnumerateOffset | Provide this for pagination. If not provided, returns the first page of results. (optional)

try:
    # Get packages
    api_response = api_instance.packages_list(body, x_authorization=x_authorization, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->packages_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[PackageQuery]**](PackageQuery.md)|  | 
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 
 **offset** | [**EnumerateOffset**](.md)| Provide this for pagination. If not provided, returns the first page of results. | [optional] 

### Return type

[**list[PackageMetadata]**](PackageMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **registry_reset**
> registry_reset(x_authorization=x_authorization)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
x_authorization = swagger_client.AuthenticationToken() # AuthenticationToken |  (optional)

try:
    api_instance.registry_reset(x_authorization=x_authorization)
except ApiException as e:
    print("Exception when calling DefaultApi->registry_reset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_authorization** | [**AuthenticationToken**](.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

