from fastapi import HTTPException, status

# файл для Exception 


class BookingException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пользователь уже существует'

class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный почта или пароль'
    
class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек'

class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен отсутсвует'

class IncorrentTokenFormException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный формат токена'

class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED