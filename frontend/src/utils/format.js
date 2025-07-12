/**
 * 格式化日期
 * @param {string|Date} date - 日期字符串或Date对象
 * @param {string} format - 格式化模式，默认为'YYYY-MM-DD HH:mm'
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm') {
  if (!date) return ''
  
  // 如果是字符串，转换为Date对象
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  // 检查日期是否有效
  if (isNaN(dateObj.getTime())) {
    console.error('Invalid date:', date)
    return ''
  }
  
  const year = dateObj.getFullYear()
  const month = String(dateObj.getMonth() + 1).padStart(2, '0')
  const day = String(dateObj.getDate()).padStart(2, '0')
  const hours = String(dateObj.getHours()).padStart(2, '0')
  const minutes = String(dateObj.getMinutes()).padStart(2, '0')
  const seconds = String(dateObj.getSeconds()).padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化文件大小
 * @param {number} bytes - 文件大小（字节）
 * @param {number} decimals - 小数位数，默认为2
 * @returns {string} 格式化后的文件大小
 */
export function formatFileSize(bytes, decimals = 2) {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i]
}

/**
 * 截断文本
 * @param {string} text - 原始文本
 * @param {number} maxLength - 最大长度
 * @param {string} suffix - 后缀，默认为'...'
 * @returns {string} 截断后的文本
 */
export function truncateText(text, maxLength, suffix = '...') {
  if (!text) return ''
  if (text.length <= maxLength) return text
  
  return text.substring(0, maxLength) + suffix
}

/**
 * 移除HTML标签
 * @param {string} html - 包含HTML标签的字符串
 * @returns {string} 移除HTML标签后的纯文本
 */
export function stripHtml(html) {
  if (!html) return ''
  
  // 创建临时DOM元素
  const temp = document.createElement('div')
  temp.innerHTML = html
  
  // 获取纯文本内容
  return temp.textContent || temp.innerText || ''
}

/**
 * 格式化货币
 * @param {number} amount - 金额
 * @param {string} currency - 货币符号，默认为'¥'
 * @param {number} decimals - 小数位数，默认为2
 * @returns {string} 格式化后的货币字符串
 */
export function formatCurrency(amount, currency = '¥', decimals = 2) {
  if (amount === null || amount === undefined) return ''
  
  const formattedAmount = Number(amount).toFixed(decimals)
  return `${currency}${formattedAmount}`
}