def demo_middleware(next_middleware, root, info, *args, **kwds):
    if (
        info.operation.name is not None
        and info.operation.name.value != "IntrospectionQuery"
    ):
        print("Demo middleware report")
        print("    operation :", info.operation.operation)
        print("    name      :", info.operation.name.value)

    return next_middleware(root, info, *args, **kwds)
