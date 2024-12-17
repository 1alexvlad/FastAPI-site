from fastapi import HTTPException, status


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
    
class HotelsIsNotFound(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Отели не найдены'

class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Невозможно забронировать отель сроком более месяца'

class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail='Не осталось свободных номеров'

class BookingWasNotFound(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Бронирование не найдено'

class DateFromCannotBeAfterDateTo(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Дата заезда не может быть позже даты выезда"

class TokenRefreshException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Refresh token не найден'