from app.db import db
from datetime import datetime

class AchievementUtils:
    @staticmethod
    def check_first_journey_achievement(user_id):
        """Check if user has earned the 'Journey Beginner' achievement"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Journey Beginner'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Check journey count
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM journeys
                WHERE user_id = %s
            """, (user_id,))
            if cursor.fetchone()['count'] == 1:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'Journey Beginner'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_event_creator_achievement(user_id):
        """Check if user has earned the 'Event Creator' achievement"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Event Creator'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Check event count
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM events e
                JOIN journeys j ON e.journey_id = j.journey_id
                WHERE j.user_id = %s
            """, (user_id,))
            if cursor.fetchone()['count'] == 1:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'Event Creator'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_first_comment_achievement(user_id):
        """Check if user has earned the 'First Comment' achievement"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'First Comment'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Check comment count
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM event_comments
                WHERE user_id = %s
            """, (user_id,))
            if cursor.fetchone()['count'] == 1:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'First Comment'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_first_share_achievement(user_id):
        """Check if user has earned the 'First Share' achievement"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'First Share'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Check public journey count
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM journeys
                WHERE user_id = %s AND status = 'public'
            """, (user_id,))
            if cursor.fetchone()['count'] == 1:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'First Share'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_discovery_pioneer_achievement(user_id, journey_id):
        """Check if user is the first to view a newly shared journey"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Discovery Pioneer'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Get journey info
            cursor.execute("""
                SELECT user_id, status, created_at 
                FROM journeys 
                WHERE journey_id = %s
            """, (journey_id,))
            journey = cursor.fetchone()
            
            if not journey or journey['user_id'] == user_id:
                return False

            # Check if first view
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM journey_views
                WHERE journey_id = %s
            """, (journey_id,))
            if cursor.fetchone()['count'] == 1:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'Discovery Pioneer'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_location_explorer_achievement(user_id):
        """Check if user has earned the 'Location Explorer' achievement (5 unique locations)"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Location Explorer'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Count unique locations
            cursor.execute("""
                SELECT COUNT(DISTINCT location) as count
                FROM events e
                JOIN journeys j ON e.journey_id = j.journey_id
                WHERE j.user_id = %s
            """, (user_id,))
            if cursor.fetchone()['count'] >= 5:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'Location Explorer'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_sharing_guru_achievement(user_id):
        """Check if user has earned the 'Sharing Guru' achievement (5 public journeys)"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Sharing Guru'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Count public journeys
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM journeys
                WHERE user_id = %s AND status = 'public'
            """, (user_id,))
            if cursor.fetchone()['count'] >= 5:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'Sharing Guru'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def get_achievement_notification(achievement_name):
        """Get achievement notification details"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT name, description, icon_url
                FROM achievements
                WHERE name = %s
            """, (achievement_name,))
            return cursor.fetchone()

    @staticmethod
    def check_popular_traveller_achievement(user_id):
        """Check if user has earned the 'Popular Traveller' achievement (5 likes)"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Popular Traveller'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Count likes on all events owned by user
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM event_reactions er
                JOIN events e ON er.event_id = e.event_id
                JOIN journeys j ON e.journey_id = j.journey_id
                WHERE j.user_id = %s AND er.reaction_type = 'like'
            """, (user_id,))
            if cursor.fetchone()['count'] >= 5:
                # Get and unlock achievement
                cursor.execute("""
                    SELECT achievement_id, name FROM achievements
                    WHERE name = 'Popular Traveller'
                """)
                achievement = cursor.fetchone()
                if achievement:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (user_id, achievement_id, is_unlocked, unlocked_at)
                        VALUES (%s, %s, 1, %s)
                    """, (user_id, achievement['achievement_id'], datetime.now()))
                    # Insert announcement
                    cursor.execute("""
                        INSERT INTO announcements (user_id, title, content, status, level, created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        "Achievement Unlocked",
                        f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                        "active",
                        "low",
                        datetime.now()
                    ))
                    return True
        return False

    @staticmethod
    def check_long_voyager_achievement(user_id, journey_id):
        """Check if user has earned the 'Long Voyager' achievement (journey > 30 days)"""
        with db.get_cursor() as cursor:
            # Skip if already earned
            cursor.execute("""
                SELECT 1 FROM user_achievements ua
                JOIN achievements a ON ua.achievement_id = a.achievement_id
                WHERE ua.user_id = %s AND a.name = 'Long Voyager'
            """, (user_id,))
            if cursor.fetchone():
                return False

            # Get min/max event start_time for this journey
            cursor.execute("""
                SELECT MIN(start_time) as min_time, MAX(start_time) as max_time
                FROM events
                WHERE journey_id = %s
            """, (journey_id,))
            times = cursor.fetchone()
            if times and times['min_time'] and times['max_time']:
                min_time = times['min_time']
                max_time = times['max_time']
                if (max_time - min_time).days > 30:
                    # Get and unlock achievement
                    cursor.execute("""
                        SELECT achievement_id, name FROM achievements
                        WHERE name = 'Long Voyager'
                    """)
                    achievement = cursor.fetchone()
                    if achievement:
                        cursor.execute("""
                            INSERT INTO user_achievements 
                            (user_id, achievement_id, is_unlocked, unlocked_at)
                            VALUES (%s, %s, 1, %s)
                        """, (user_id, achievement['achievement_id'], datetime.now()))
                        # Insert announcement
                        cursor.execute("""
                            INSERT INTO announcements (user_id, title, content, status, level, created_time)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (
                            user_id,
                            "Achievement Unlocked",
                            f"Congratulations! You unlocked the '{achievement['name']}' achievement.",
                            "active",
                            "low",
                            datetime.now()
                        ))
                        return True
        return False 