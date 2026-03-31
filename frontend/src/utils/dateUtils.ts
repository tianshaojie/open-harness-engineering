/**
 * 日期时间格式化工具函数
 * 统一管理所有日期时间格式化相关功能
 */

/**
 * 格式化日期时间（不包含秒）
 * @param dateString 日期字符串
 * @returns 格式化后的日期时间字符串，格式：YYYY/MM/DD HH:mm
 */
export const formatDateTime = (dateString: string | null | undefined): string => {
  if (!dateString) return '-';

  try {
    const date = new Date(dateString);
    
    if (isNaN(date.getTime())) {
      return '-';
    }

    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return '-';
  }
};

/**
 * 格式化日期时间（包含秒）
 * @param timeStr 日期字符串
 * @returns 格式化后的日期时间字符串，格式：YYYY/MM/DD HH:mm:ss
 */
export const formatTime = (timeStr: string | null | undefined): string => {
  if (!timeStr) return '-';
  
  try {
    const date = new Date(timeStr);
    
    if (isNaN(date.getTime())) {
      return '-';
    }
    
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return '-';
  }
};
