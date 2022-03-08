import channels
import channels_graphql_ws
import graphene
from graphql_auth.schema import UserQuery, MeQuery

import core.schema


# import core.schema.Mutation
from pet_project.middleware import demo_middleware
from users.schema import AuthMutation


class Query(
    core.schema.Query,
    UserQuery,
    MeQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    core.schema.Mutation,
    AuthMutation,
    graphene.ObjectType
):
    pass


class Subscription(
    core.schema.Subscription
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    async def on_connect(self, payload):
        """Handle WebSocket connection event."""

        self.scope["user"] = await channels.auth.get_user(self.scope)

    schema = schema
    middleware = [demo_middleware]
