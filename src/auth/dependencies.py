# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, JWTError
# import httpx
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric import rsa
# import base64
# from typing import Collection, List, Dict, Any
# from src.errors.base_error_code import BaseErrorCode
# from src.errors.base_exception import BaseException
# from .config import auth_config
# from .models import User

# security = HTTPBearer()

# class KeycloakJwtAuthenticationConverter:
#     """
#     Converter chính xác theo Java code của bạn
#     implements Converter<Jwt, AbstractAuthenticationToken>
#     """
    
#     def __init__(self):
#         self.jwks_uri = f"{auth_config.issuer_uri}/protocol/openid-connect/certs"
#         self._cached_jwks = None
    
#     async def get_jwks(self):
#         """Lấy JWKS từ Keycloak - Spring Security làm auto, chúng ta làm thủ công"""
#         if self._cached_jwks is None:
#             async with httpx.AsyncClient() as client:
#                 response = await client.get(self.jwks_uri)
#                 response.raise_for_status()
#                 self._cached_jwks = response.json()
#         return self._cached_jwks
    
#     def get_public_key(self, jwks: dict, token: str):
#         """Lấy public key từ JWKS dựa trên kid trong JWT header"""
#         headers = jwt.get_unverified_header(token)
#         kid = headers.get('kid')
        
#         for key in jwks.get('keys', []):
#             if key.get('kid') == kid and key.get('kty') == 'RSA':
#                 # Convert JWK to RSA public key (giống Spring Security)
#                 n = int.from_bytes(base64.urlsafe_b64decode(key['n'] + '=='), 'big')
#                 e = int.from_bytes(base64.urlsafe_b64decode(key['e'] + '=='), 'big')
                
#                 public_key = rsa.RSAPublicNumbers(e, n).public_key(default_backend())
#                 return public_key
        
#         raise BaseException(error_code= BaseErrorCode.UNAUTHORIZED, message="Public key not found for given kid") 

#     def extract_resource_roles(self, jwt_payload: dict) -> Collection[str]:
#         """
#         CHÍNH XÁC theo Java code của bạn:
#         private Collection<? extends GrantedAuthority> extractResourceRoles(Jwt jwt)
#         """
#         # Logic to extract roles from the JWT token - GIỐNG HỆT JAVA
#         resource_access = dict(jwt_payload.get("resource_access", {}))
        
#         # var eternal = (Map<String, List<String>>) resource_access.get("account");
#         eternal = resource_access.get("account")
#         if eternal and isinstance(eternal, dict):
#             # var roles = eternal.get("roles");
#             roles = eternal.get("roles", [])
            
#             # return roles.stream()
#             #     .map(role -> new SimpleGrantedAuthority("ROLE_" + role.replace("-", "_").toUpperCase()))
#             #     .toList();
#             return [
#                 f"ROLE_{role.replace('-', '_').upper()}" 
#                 for role in roles
#             ]
        
#         return []

#     async def convert(self, token: str) -> User:
#         """
#         CHÍNH XÁC theo Java code:
#         public AbstractAuthenticationToken convert(@NonNull Jwt source)
        
#         Trong Java: return new JwtAuthenticationToken(source, Stream.concat(...))
#         Trong Python: return User với roles đã được merge
#         """
#         try:
#             # Lấy JWKS
#             jwks = await self.get_jwks()
#             public_key = self.get_public_key(jwks, token)
            
#             # Decode JWT
#             payload = jwt.decode(
#                 token,
#                 public_key,
#                 algorithms=["RS256"],
#                 issuer=auth_config.issuer_uri
#             )
            
#             # GIỐNG HỆT JAVA CODE:
#             # Stream.concat(
#             #   new JwtGrantedAuthoritiesConverter().convert(source).stream(),  // realm_access roles
#             #   extractResourceRoles(source).stream()                           // resource_access roles  
#             # ).collect(Collectors.toSet())
            
#             # 1. Realm roles (JwtGrantedAuthoritiesConverter trong Spring)
#             realm_roles = []
#             realm_access = payload.get('realm_access', {})
#             if isinstance(realm_access, dict):
#                 realm_roles = [
#                     f"ROLE_{role.replace('-', '_').upper()}" 
#                     for role in realm_access.get('roles', [])
#                 ]
            
#             # 2. Resource roles (extractResourceRoles trong Java)
#             resource_roles = self.extract_resource_roles(payload)
            
#             # Merge và loại bỏ trùng lặp - giống Java .collect(Collectors.toSet())
#             all_roles = list(set(realm_roles + resource_roles))
            
#             return User(
#                 id=payload.get('sub'),
#                 username=payload.get('preferred_username', ''),
#                 email=payload.get('email', ''),
#                 roles=all_roles
#             )
            
#         except JWTError as e:
#             raise BaseException(error_code= BaseErrorCode.UNAUTHORIZED, message="Failed to decode JWT") from e

# # Khởi tạo converter
# converter = KeycloakJwtAuthenticationConverter()

# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ) -> User:
#     """
#     Dependency để inject user vào routes
#     Tương tự @AuthenticationPrincipal trong Spring
#     """
#     if credentials.scheme != "Bearer":
#         raise BaseException(error_code= BaseErrorCode.UNAUTHORIZED, message="Invalid authentication scheme")
    
#     return await converter.convert(credentials.credentials)

# def require_role(required_role: str):
#     """
#     Role-based authorization 
#     Tương tự @PreAuthorize("hasRole('ROLE_ADMIN')") trong Spring
#     """
#     async def role_checker(user: User = Depends(get_current_user)):
#         if required_role not in user.roles:
#             raise BaseException(error_code= BaseErrorCode.NO_ACCESS, message="Access denied")
#         return user
#     return role_checker