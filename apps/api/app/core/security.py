from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

EDITORIAL_ADMIN_EMAIL = "alves2.eduardo@gmail.com"
bearer_scheme = HTTPBearer(auto_error=False)


def require_editorial_admin(
	credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
	if credentials is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Autenticação necessária.",
			headers={"WWW-Authenticate": "Bearer"},
		)

	try:
		claims = auth.verify_id_token(credentials.credentials, check_revoked=True)
	except (
		auth.InvalidIdTokenError,
		auth.ExpiredIdTokenError,
		auth.RevokedIdTokenError,
		auth.CertificateFetchError,
		FirebaseError,
		ValueError,
	) as error:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token Firebase inválido ou expirado.",
			headers={"WWW-Authenticate": "Bearer"},
		) from error

	email = str(claims.get("email", "")).strip().casefold()
	if claims.get("email_verified") is not True or email != EDITORIAL_ADMIN_EMAIL:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Esta conta não tem permissão editorial.",
		)

	return claims
