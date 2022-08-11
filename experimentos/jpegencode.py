
def jpeg_encode(frame):
    success, jpeg = cv2.imencode('.jpg', frame)

    return jpeg.tobytes()