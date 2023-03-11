# PackageData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** | Package contents. This is the zip file uploaded by the user. (Encoded as text using a Base64 encoding).  This will be a zipped version of an npm package&#x27;s GitHub repository, minus the \&quot;.git/\&quot; directory.\&quot; It will, for example, include the \&quot;package.json\&quot; file that can be used to retrieve the project homepage.  See https://docs.npmjs.com/cli/v7/configuring-npm/package-json#homepage. | [optional] 
**url** | **str** | Package URL (for use in public ingest). | [optional] 
**js_program** | **str** | A JavaScript program (for use with sensitive modules). | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

