# DATABASE_URL_TEST = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
#
# engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
# async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
# metadata.bind = engine_test
#
#
# async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
# app.dependency_overrides[get_async_session] = override_get_async_session