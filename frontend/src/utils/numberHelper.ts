/**
 * 将科学计数法转换为完整数字字符串，并可选择格式化为CSV文本格式
 * 仅对 number 类型做展开；字符串（如 app_code "641787E3"）原样返回，避免标识符被误当科学计数法。
 * @param value - 需要转换的值（数字或字符串）
 * @param options - 配置选项
 * @param options.forCSV - 是否格式化为CSV文本格式（添加制表符前缀，强制Excel识别为文本）
 * @returns 转换后的完整数字字符串，若不是数字类型的科学计数法则返回原始字符串
 */
export function convertScientificNotation(value: any, options?: { forCSV?: boolean }): string {
  // 处理 null 和 undefined
  if (value === null || value === undefined) {
    return '';
  }

  const forCSV = options?.forCSV ?? false;

  // 仅对 number 类型做科学计数法展开；字符串（如接口返回的 app_code "641787E3"）原样返回
  if (typeof value !== 'number') {
    const str = String(value);
    return forCSV && /^-?\d*\.?\d+$/.test(str) ? `\t${str}` : str;
  }

  const str = String(value);

  // 检查是否是科学计数法（包含 'e' 或 'E'）
  if (!str.includes('e') && !str.includes('E')) {
    return forCSV && /^-?\d*\.?\d+$/.test(str) ? `\t${str}` : str;
  }

  // 解析科学计数法格式：base e exponent
  const match = str.match(/^([+-]?\d*\.?\d+)[eE]([+-]?\d+)$/);
  if (!match) {
    return forCSV && /^-?\d*\.?\d+$/.test(str) ? `\t${str}` : str;
  }

  // 计算科学计数法的实际值
  const base = parseFloat(match[1]);
  const exponent = parseInt(match[2], 10);
  const numResult = base * Math.pow(10, exponent);

  let result: string;
  if (Number.isInteger(numResult)) {
    if (Math.abs(numResult) > Number.MAX_SAFE_INTEGER) {
      try {
        result = BigInt(numResult).toString();
      } catch {
        result = numResult.toFixed(0);
      }
    } else {
      result = numResult.toString();
    }
  } else {
    result = numResult.toString();
  }

  return forCSV && /^-?\d*\.?\d+$/.test(result) ? `\t${result}` : result;
}
