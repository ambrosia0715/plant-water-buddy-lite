// lib/core/utils/date_formats.dart
import 'package:intl/intl.dart';

class DateFormats {
  // yyyy.MM.dd (E) 형식
  static String formatWithWeekday(DateTime date) {
    final formatter = DateFormat('yyyy.MM.dd (E)', 'ko_KR');
    return formatter.format(date);
  }

  // yyyy.MM.dd 형식
  static String formatSimple(DateTime date) {
    final formatter = DateFormat('yyyy.MM.dd');
    return formatter.format(date);
  }

  // D-day 표기
  static String getDDayText(int daysUntil) {
    if (daysUntil == 0) {
      return '오늘';
    } else if (daysUntil == 1) {
      return 'D-1';
    } else if (daysUntil > 0) {
      return 'D-$daysUntil';
    } else {
      final overdue = daysUntil.abs();
      return '+$overdue일 밀림';
    }
  }

  // 상대 시간 표기
  static String getRelativeTimeText(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inDays > 7) {
      return formatSimple(dateTime);
    } else if (difference.inDays > 0) {
      return '${difference.inDays}일 전';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}시간 전';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}분 전';
    } else {
      return '방금';
    }
  }

  // 시간 포맷 (오전/오후 h:mm)
  static String formatTime(int hour, int minute) {
    final period = hour >= 12 ? '오후' : '오전';
    final displayHour = hour > 12 ? hour - 12 : (hour == 0 ? 12 : hour);
    return '$period ${displayHour}:${minute.toString().padLeft(2, '0')}';
  }
}
