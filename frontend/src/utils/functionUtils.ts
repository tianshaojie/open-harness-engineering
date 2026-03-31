/**
 * 函数工具类
 * 提供防抖、节流等函数处理工具
 */

/**
 * 防抖函数 - 限制函数在一定时间内只执行一次
 * @param fn 需要防抖的函数
 * @param delay 延迟时间，单位毫秒
 * @returns 防抖处理后的函数
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: number | null = null;
  
  return function(this: any, ...args: Parameters<T>): void {
    if (timer) {
      window.clearTimeout(timer);
    }
    
    timer = window.setTimeout(() => {
      fn.apply(this, args);
      timer = null;
    }, delay);
  };
}

/**
 * 节流函数 - 限制函数在一定时间内的执行频率
 * @param fn 需要节流的函数
 * @param delay 延迟时间，单位毫秒
 * @returns 节流处理后的函数
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastCallTime = 0;
  let timer: number | null = null;
  
  return function(this: any, ...args: Parameters<T>): void {
    const now = Date.now();
    const timeSinceLastCall = now - lastCallTime;
    
    if (timeSinceLastCall >= delay) {
      // 立即执行
      lastCallTime = now;
      fn.apply(this, args);
    } else {
      // 延迟执行
      if (timer) {
        window.clearTimeout(timer);
      }
      timer = window.setTimeout(() => {
        lastCallTime = Date.now();
        fn.apply(this, args);
        timer = null;
      }, delay - timeSinceLastCall);
    }
  };
}

