@description('Name of the Grounding with Bing resource')
param bingName string

@description('Tags to apply to resources')
param tags object = {}

@description('Name of the Foundry resource')
param foundryName string

#disable-next-line BCP081
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: foundryName
  scope: resourceGroup()
}

resource bingGrounding 'Microsoft.Bing/accounts@2025-05-01-preview' = {
  name: bingName
  location: 'global'
  tags: tags
  kind: 'Bing.Grounding'
  sku: {
    name: 'G1'
  }
  properties: {}
}

#disable-next-line BCP081
resource bingConnection 'Microsoft.CognitiveServices/accounts/connections@2025-04-01-preview' = {
  name: '${foundryName}-bingsearchconnection'
  parent: foundryAccount
  properties: {
    category: 'ApiKey'
    target: 'https://api.bing.microsoft.com/'
    authType: 'ApiKey'
    credentials: {
      key: '${listKeys(bingGrounding.id, '2020-06-10').key1}'
    }
    isSharedToAll: true
    metadata: {
      ApiType: 'Azure'
      Location: bingGrounding.location
      ResourceId: bingGrounding.id
    }
  }
}

output bingName string = bingGrounding.name
output bingId string = bingGrounding.id
