from pydantic_settings import BaseSettings


class KeycloakConfig(BaseSettings):
    realm: str = "demo-realm"
    issuer_uri: str = f"http://localhost:8080/realms/{realm}"

    class Config:
        env_file = ".env"


keycloak_config = KeycloakConfig()
