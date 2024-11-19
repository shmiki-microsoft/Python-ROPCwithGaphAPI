"""
graph sdk for python example
"""
import os
import asyncio
from azure.identity import UsernamePasswordCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph_core.tasks.page_iterator import PageIterator

credentials = UsernamePasswordCredential(
    client_id=os.getenv('clientId'),
    username=os.getenv('userName'),
    password=os.getenv('userPassword')
)
scopes = ['https://graph.microsoft.com/.default']
client = GraphServiceClient(credentials=credentials, scopes=scopes)

async def get_user():
    """get user"""
    users = await client.users.get()
    if users:
        for user in users.value:
            print(f"user.user_principal_name:{user.user_principal_name}")

async def get_user_paging():
    """get user with paging
    To initialize your graph_client, 
    see https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python
    """
    query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            top = 1,
    )
    request_configuration = RequestConfiguration(
    query_parameters = query_params,
    )

    users = await client.users.get(request_configuration = request_configuration)
    while users is not None and users.odata_next_link is not None:
        users = await client.users.with_url(users.odata_next_link).get()
        if users:
            print(f"########## users:")
            for user in users.value:
                print(f"user.user_principal_name:{user.user_principal_name}")

def callback(user):
    """callback"""
    print(f'{user.user_principal_name=}')
    return True

async def iterate_all_users():
    """iterate all users
    https://github.com/microsoftgraph/msgraph-sdk-python-core/pull/479
    """
    query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
        select = ["userPrincipalName"],
        top = 1,
    )
    config = RequestConfiguration(
        query_parameters = query_params,
    )
    users = await client.users.get(config)
    page_iterator = PageIterator(users, client.request_adapter)
    await page_iterator.iterate(callback)

asyncio.run(iterate_all_users())
