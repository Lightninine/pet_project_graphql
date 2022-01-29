import graphene
from graphql_auth.schema import UserQuery, MeQuery

import core.schema


# import core.schema.Mutation
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


schema = graphene.Schema(query=Query, mutation=Mutation)
