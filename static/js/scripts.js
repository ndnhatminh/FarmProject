function deleteSchedule(scheduleId) {
    fetch('/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: scheduleId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Xử lý phản hồi từ API nếu cần
        console.log(data);
        // Có thể làm một số thao tác khác, như cập nhật giao diện người dùng
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}