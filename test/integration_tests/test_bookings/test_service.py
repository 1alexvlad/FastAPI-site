from bookings.service import BookingService
from datetime import datetime
async def test_add_and_get_booking():
    new_booking = await BookingService.add(
        user_id=2, 
        room_id=2,
        date_from=datetime.strptime("2023-07-15", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-25", "%Y-%m-%d"),
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2
    new_booking = await BookingService.find_by_id(new_booking.id)
    
    assert new_booking is not None