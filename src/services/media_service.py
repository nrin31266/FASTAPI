from sqlalchemy.orm import Session
from src import dto, models
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.cloud  import cloud_service
import yt_dlp
import os
from datetime import datetime

# ==========================================================
# PHẦN LẤY THÔNG TIN (INFO EXTRACTOR)
# ==========================================================
YDL_INFO_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
    'extract_flat': 'in_playlist',
}
ydl_info_extractor = yt_dlp.YoutubeDL(YDL_INFO_OPTS)


# ==========================================================
# PHẦN TẢI VỀ (DOWNLOADER)
# ==========================================================

# 1. ĐỊNH NGHĨA NƠI LƯU FILE (QUAN TRỌNG)
# Đây là nơi file MP3 sẽ được lưu.
# Hãy thay bằng đường dẫn tuyệt đối trên server của bạn.
# Ví dụ: '/var/www/my-app/media/' hoặc đọc từ biến môi trường
AUDIO_SAVE_PATH = os.getenv('AUDIO_SAVE_PATH', '/tmp/audio_files')

# Tạo thư mục này nếu nó chưa tồn tại
os.makedirs(AUDIO_SAVE_PATH, exist_ok=True)


# 2. CẤU HÌNH ĐỂ TẢI MP3
YDL_DOWNLOAD_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
    'format': 'bestaudio/best', # Chỉ tải âm thanh tốt nhất
    
    # Đây là câu trả lời cho "lưu vào đâu":
    # '%(id)s' sẽ được thay bằng ID của video (ví dụ: dQw4w9WgXcQ)
    # '%(ext)s' sẽ là 'mp3' (do postprocessor bên dưới)
    'outtmpl': f'{AUDIO_SAVE_PATH}/%(id)s.%(ext)s',
    
    # Cấu hình chuyển đổi sang MP3 (Yêu cầu FFmpeg)
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192', # Chất lượng 192kbps
    }],
}

# 3. TẠO ĐỐI TƯỢNG DOWNLOADER TOÀN CỤC
ydl_downloader = yt_dlp.YoutubeDL(YDL_DOWNLOAD_OPTS)


def download_audio(rq: dto.MediaAudioCreateRequest, db: Session) -> dto.MediaAudioResponse:
    # Giả sử bạn có logic để tải audio từ YouTube hoặc xử lý file audio ở đây
    # Ví dụ đơn giản: tạo một bản ghi MediaAudio trong database
    if(rq.input_type not in ['youtube', 'audio_file']):
        raise BaseException(BaseErrorCode.BAD_REQUEST, message="Invalid input type")
    
    process_info = None
    
    if(rq.input_type == 'youtube'):
        process_info = download_youtube_audio(rq, db)
    elif(rq.input_type == 'audio_file'):
        process_info = download_audio_file(rq, db)
        
    media_audio = models.MediaAudio(
        input_url = rq.input_url,
        input_type = rq.input_type,
        duration = process_info['duration'] if process_info else 0,
        title = process_info['title'] if process_info else '',
    )
    # Upload file to Cloudinary
    file_path = process_info['file_path']
    video_id = os.path.splitext(os.path.basename(file_path))[0]
    public_id = f"fastapi/test1/audio_files/" + video_id + "_" + datetime.now().strftime("%Y%m%d%H%M%S")

    upload_result = upload_audio_file(file_path, public_id)
    if not upload_result:
        raise BaseException(BaseErrorCode.INTERNAL_SERVER_ERROR, message="Upload file lên Cloudinary thất bại.")
    print(f"File đã được upload lên Cloudinary: {upload_result}")
    
    media_audio.file_path = upload_result

    db.add(media_audio)
    db.commit()
    db.refresh(media_audio)
    print("Đã lưu thông tin MediaAudio vào database.")
    # Sau khi lưu xong, trả về DTO 
    return dto.MediaAudioResponse.model_validate(media_audio)

def download_youtube_audio(rq: dto.MediaAudioCreateRequest, db: Session):
    print("Đang lấy thông tin video...")
    
    try:
        # ==========================================================
        # PHẦN 1: LẤY THÔNG TIN
        # ==========================================================
        info = ydl_info_extractor.extract_info(rq.input_url, download=False)
        
        print("\n--- Thông tin Video ---")
        print(f"Tiêu đề: {info['title']}")
        print(f"Thời lượng: {info['duration_string']}")

        # Kiểm tra thời lượng (sửa lỗi cú pháp của bạn)
        duration_sec = info.get('duration', 0)
        if duration_sec > 600: # Lớn hơn 10 phút (600 giây)
            raise BaseException(BaseErrorCode.BAD_REQUEST, 
                                message=f"Video quá dài ({duration_sec}s). Chỉ chấp nhận video dưới 10 phút.")

        # ==========================================================
        # PHẦN 2: TẢI FILE MP3
        # ==========================================================
        print(f"Video hợp lệ (Thời lượng: {duration_sec}s). Bắt đầu tải...")

        # Gọi download bằng đối tượng downloader toàn cục
        # Tác vụ này sẽ block cho đến khi tải và convert xong
        ydl_downloader.download([rq.input_url])

        # Xây dựng đường dẫn file cuối cùng (để lưu vào DB)
        video_id = info.get('id')
        final_mp3_path = f"{AUDIO_SAVE_PATH}/{video_id}.mp3"
        
        print(f"Đã tải và convert thành công: {final_mp3_path}")
        
        # Tạm thời trả về thông tin file đã
        return {
            "file_path": final_mp3_path,
            "title": info.get('title'),
            "duration": duration_sec
        }

    except yt_dlp.utils.DownloadError as e:
        raise BaseException(BaseErrorCode.BAD_REQUEST, message=f"Lỗi khi xử lý video: {str(e)}")
    except Exception as e:
        raise BaseException(BaseErrorCode.INTERNAL_SERVER_ERROR, message=f"Lỗi hệ thống: {str(e)}")

def download_audio_file(rq: dto.MediaAudioCreateRequest, db: Session):

    return None

def upload_audio_file(file_path: str, public_id: str):

    return cloud_service.upload_file(file_path, public_id, resource_type="video")  # audio được coi như video