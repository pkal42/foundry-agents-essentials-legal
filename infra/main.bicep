targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the environment (used for resource naming)')
param environmentName string

@description('Primary Azure region for resources')
param location string = resourceGroup().location

@description('Principal ID of the user who needs Foundry access (defaults to the deployer)')
param foundryUserPrincipalId string = deployer().objectId

var tags = {
  'azd-env-name': environmentName
}

var resourceToken = toLower(uniqueString(resourceGroup().id, environmentName, location))

module appService 'modules/app-service.bicep' = {
  name: 'app-service'
  params: {
    appServicePlanName: 'plan-${resourceToken}'
    webAppName: 'app-${resourceToken}'
    location: location
    tags: tags
  }
}

module foundry 'modules/foundry.bicep' = {
  name: 'foundry'
  params: {
    accountName: 'foundry-${resourceToken}'
    projectName: 'onboarding-lab'
    location: location
    tags: tags
  }
}

module bingGrounding 'modules/bing-grounding.bicep' = {
  name: 'bing-grounding'
  params: {
    bingName: 'bing-${resourceToken}'
    foundryName: foundry.outputs.accountName
    tags: tags
  }
}

module search 'modules/search.bicep' = {
  name: 'search'
  params: {
    searchName: 'search-${resourceToken}'
    location: location
    tags: tags
  }
}

module roleAssignments 'modules/role-assignments.bicep' = {
  name: 'role-assignments'
  params: {
    principalId: appService.outputs.webAppPrincipalId
    foundryId: foundry.outputs.accountId
  }
}

module userRoleAssignments 'modules/role-assignments.bicep' = {
  name: 'user-role-assignments'
  params: {
    principalId: foundryUserPrincipalId
    principalType: 'User'
    foundryId: foundry.outputs.accountId
  }
}

output AZURE_RESOURCE_GROUP string = resourceGroup().name
output AZURE_WEBAPP_NAME string = appService.outputs.webAppName
output AZURE_WEBAPP_URL string = appService.outputs.webAppUrl
output AZURE_FOUNDRY_NAME string = foundry.outputs.accountName
output AZURE_FOUNDRY_ENDPOINT string = foundry.outputs.accountEndpoint
output AZURE_BING_NAME string = bingGrounding.outputs.bingName
output AZURE_SEARCH_NAME string = search.outputs.searchName
output AZURE_SEARCH_ENDPOINT string = search.outputs.searchEndpoint
