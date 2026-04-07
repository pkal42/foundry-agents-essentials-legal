@description('Principal ID to assign the role to')
param principalId string

@description('Principal type')
param principalType string = 'ServicePrincipal'

@description('Resource ID of the Foundry account')
param foundryId string

// Cognitive Services User
var cognitiveServicesUserRoleId = 'a97b65f3-24c7-4388-baec-2e87135dc908'

// Azure AI User
var azureAIUserRoleId = '53ca6127-db72-4b80-b1b0-d745d6d5456d'

// Azure AI Account Owner — needed only for Guardrails (Unit 7)
var azureAIAccountOwnerRoleId = 'b78c5d69-af96-48a3-bf8d-a8f1cb6a0e60'

resource foundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: last(split(foundryId, '/'))
}

resource cognitiveServicesUserRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundryId, principalId, cognitiveServicesUserRoleId)
  scope: foundry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesUserRoleId)
    principalId: principalId
    principalType: principalType
  }
}

resource azureAIUserRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundryId, principalId, azureAIUserRoleId)
  scope: foundry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', azureAIUserRoleId)
    principalId: principalId
    principalType: principalType
  }
}

// Needed only for Guardrails (Unit 7)
resource azureAIAccountOwnerRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundryId, principalId, azureAIAccountOwnerRoleId)
  scope: foundry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', azureAIAccountOwnerRoleId)
    principalId: principalId
    principalType: principalType
  }
}
