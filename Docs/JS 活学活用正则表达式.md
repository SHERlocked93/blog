# JS 活学活用正则表达式

记录一些项目中用到的正则工具，将持续更新...

如果对JS中的正则不太了解，可以参考一下[JS 中正则表达式必知必会](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E5%BF%85%E7%9F%A5%E5%BF%85%E4%BC%9A.md)

## 1. 字符串操作

### 1.1 去除字符串两边的空格 trim

```text
String.prototype.trim = function() {
  return this.replace(/(^\s+)\|(\s+$)/g, '')
}
```

### 1.2 HTML编码对`< > ' " &`等字符转义，避免XSS攻击

```text
function htmlEncode(str) {
  return str.replace(/[\<\>\"\'\&]/g, function(rs) {
    switch (rs) {
      case '<':
        return '&lt;'
      case '>':
        return '&gt;'
      case '&':
        return '&amp;'
      case ''':
        return '&apos;'
      case '"':
        return '&quot;'
    }
  })
}
```

### 1.3 找出重复最多的字符

```text
let str = 'asss23sjdssskssa7lsssdkjsssdss'
const arr = str.split(/\s*/)                          // 把字符串转换为数组
const str2 = arr.sort().join('')                         // 首先进行排序，这样结果会把相同的字符放在一起，然后再转换为字符串
let value = ''
let index = 0
str2.replace(/(\w)\1*/g, function($0, $1) {                 // 匹配字符
  if (index < $0.length) {
    index = $0.length                          // index是出现次数
    value = $1                                 // value是对应字符
  }
})
console.log(`最多的字符: ${value} ,重复的次数: ${index}`)                 // s 17
```

### 1.4 数字格式化，1234567890 -> 1,234,567,890

下面简单分析下正则`/\B(?=(\d{3})+(?!\d))/g`：

1. `/\B(?=(\d{3})+(?!\d))/g`：正则匹配非单词边界`\B`，边界后面必须跟着`(\d{3})+(?!\d)`
2. `(\d{3})+`：必须是1个或多个的3个连续数字
3. `(?!\d)`：第2步中的3个数字不允许后面跟着数字
4. `(\d{3})+(?!\d)`：所以匹配的边界后面必须跟着3*n（n>=1）的数字

最终把匹配到的所有边界换成`,`即可

```text
const numFormat = str => str.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
```

### 1.5 手机号中间四位换*

手机号中间4位数换成*

```text
const validateMobile = str =>  /^[1][0-9]{10}$/.test(str) && str.replace(/(\d{3})(\d{4})(\d{4})/, (rs, $1, $2, $3) => `${$1}****${$3}`)
```

### 1.6 取URL中query到一个对象中

```text
function getUrlParam(str) {
  const result = {}
  const valid = /(https?|ftp):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/.exec(str)
  if (!valid) return
  const [rs, $1, $2, $3] = valid
  $3.match(/[a-zA-Z_]+=[^=&?]*/g).forEach(val => val.replace(/^(\w+)=(\w*)$/, ($0, $1, $2) => {
        result[$1] = $2
      })
  )
  return result
}

getUrlParam('https://www.baidu.com?name=jawil&age=23&d=')         // {name: "jawil", age: "23", d: ""}
```

### 1.7 驼峰转下划线

```text
'componentMapModelRegistry'.match(/^[a-z][a-z0-9]+|[A-Z][a-z0-9]*/g).join('_').toLowerCase();
// component_map_model_registry
```

### 1.8 下划线转驼峰

```text
'component_map_model_registry'.replace(/_(\w)/g, (str, letter) => letter.toUpperCase())
// componentMapModelRegistry
```

### 1.9 获取文件名信息，提取文件名和文件名后缀

```text
export const getFileInfo = fileName => {
  const fileRe = /(.+)(\.[a-z0-9]+)$/i
  try {
    const result = fileRe.exec(fileName)
    return {
      name: result[1],
      type: result[2]
    }
  } catch (e) {
    return null
  }
}
```

## 2. 验证

用于验证时，通常需要在前后分别加上`^`、`$`、`\b`，以匹配整个待验证字符串

### 2.1 常用正则验证

```text
function checkStr(str, type) {
  switch (type) {
    case 'phone': //手机号码
      return /^1\d{10}$/.test(str)
    case 'tel': // 座机
      return /^(0\d{2,3}-\d{7,8})(-\d{1,4})?$/.test(str)
    case 'card': // 身份证
      return /^\d{15}|\d{18}$/.test(str)
    case 'pwd': // 密码以字母开头，长度在6~18之间，只能包含字母、数字和下划线
      return /^[a-zA-Z]\w{5,17}$/.test(str)
    case 'postal': // 邮政编码
      return /[1-9]\d{5}(?!\d)/.test(str)
    case 'QQ': // QQ号 5-11位数字
      return /^[1-9]\d{4,10}$/.test(str)
    case 'email': // 邮箱
      return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(str)
    case 'money': // 金额(小数点2位)
      return /^\d*(?:\.\d{0,2})?$/.test(str)
    case 'URL': // 网址
      return /(https?|ftp):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/.test(str)
    case 'IP':  // IP
      return /((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))/.test(str)
    case 'day':  // 一个月的31天  01-09和1~31
      return /^((0?[1-9])|(([12])[0-9])|30|31)$/.test(str)
    case 'month': // 一年的12个月  01-09和1-12
      return /^(0?[1-9]|1[0-2])$/.test(str)
    case 'date':  // 日期时间
      return /^(\d{4})\-(\d{2})\-(\d{2}) (\d{2})(?:\:\d{2}|:(\d{2}):(\d{2}))$/.test(str) || /^(\d{4})\-(\d{2})\-(\d{2})$/.test(str)
    case 'integer': // 整数 正整数或负整数
      return /^-?\d+$/.test(str)
    case 'decimal': // 小数
      return /^(-?\d+)(\.\d+)?$/.test(str)
    case 'english': // 英文
      return /^[a-zA-Z]+$/.test(str)
    case 'chinese': // 中文
      return /^[\u4E00-\u9FA5]+$/.test(str)
    case 'cname':  // 中文姓名 2-4位汉字
      return /^[\u4E00-\u9FA5]{2,4}$/.test(str)
    case 'lower':  // 小写
      return /^[a-z]+$/.test(str)
    case 'upper':  // 大写
      return /^[A-Z]+$/.test(str)
    case 'HTML':  // HTML标记
      return /<("[^"]*"|'[^']*'|[^'">])*>/.test(str)
    default:
      throw new Error('检验出错 in function checkStr')
  }
}
```

### 2.2 验证是否是合法URL

```text
function validateURL(textval) {
  const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
  return urlregex.test(textval)
}
```

---

> 参考：
>
> 1. [JavaScript正则进阶之路——活学妙用奇淫正则表达式](https://segmentfault.com/a/1190000009590458)
> 2. [js正则验证方法大全](https://link.segmentfault.com/?enc=M9laeKouRbUoiGH2GH%2FlzA%3D%3D.ciySGE%2FKHVuZhpL%2FzHCnnu49F7ZynSIbYoYXNDxg5aBEuCh5qu8nsVBq8%2FrjabCKE6z2ypb54Fkb2CF3fdtTBA%3D%3D)
> 3. [javascript 总结（RegExp篇）](https://segmentfault.com/a/1190000012699314)
