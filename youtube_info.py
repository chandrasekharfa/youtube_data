import yt_dlp
from datetime import datetime
from database import collection, save_video_stats_to_db, update_video_stats_in_db
from fastapi import HTTPException

async def get_youtube_video_info(url: str):

    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': False,
            'force_generic_extractor': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            
            video_data = {
                "url": url,
                "title": info_dict.get('title', 'Unknown Title'),
                "likes": info_dict.get('like_count', 'Not available'),
                "dislikes": info_dict.get('dislike_count', 'Not available'),
                "comments": info_dict.get('comment_count', 'Not available'),
                "views": info_dict.get('view_count', 'Not available'),
                "last_updated_at": datetime.utcnow(),
            }

            
            existing_video = collection.find_one({"url": url})
            if existing_video:
                update_video_stats_in_db(existing_video["_id"], video_data)
                video_id = str(existing_video["_id"])
            else:
                video_id = save_video_stats_to_db(video_data)

            return {
                "title": video_data["title"],
                "likes": video_data["likes"],
                "dislikes": video_data["dislikes"],
                "comments": video_data["comments"],
                "mongodb_id": video_id,
                "views": video_data["views"],
                "last_updated_at": video_data["last_updated_at"]
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
