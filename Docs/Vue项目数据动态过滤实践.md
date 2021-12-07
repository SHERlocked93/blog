# Vue项目数据动态过滤实践

这个问题是在下在做一个Vue项目中遇到的实际场景，这里记录一下我遇到问题之后的思考和最后怎么解决的(记性不好 -。-)，过程中会涉及到一些Vue的源码，如果不太了解的话可以瞅瞅 [Vue源码阅读系列文章](https://juejin.im/post/5b38830de51d455888216675)~

问题是这样的：页面从后台拿到的数据是由`0`、`1`之类的key，而这个key代表的value比如`0`代表女、`1`代表男的对应关系是要从另外一个数据字典接口拿到的；类似于[这样的Api](https://easy-mock.com/mock/59e6f5dd34be4b482ca23abe/ele-template/manage/config/sys-param/list-all)：

```json
{
  "SEX_TYPE": [
    { "paramValue": 0, "paramDesc": "女" },
    { "paramValue": 1, "paramDesc": "男" }
  ]
}
```

那么如果view拿到的是`0`，就要从字典中找到它的描述`女`并且显示出来；下面故事开始了

## 1. 思考

有人说，这不是过滤器 `filter` 要做的事么，直接filter不就行了，然而问题是这个filter是要等待异步的数据字典接口返回之后才能拿到，如果在component编译的时候这个filter没有找到，那么就会导致错误影响之后的渲染(白屏并报undefined错)；

我想到的解决方法有两个，一是接口变为[同步](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/Synchronous_and_Asynchronous_Requests)，在`beforeCreate`或`created`钩子中同步地获取数据字典接口，保证在 `$mount`的时候可以拿到注册好的filter，保证时序，但是这样会阻塞挂载，延长白屏时间，因此不推介；二是把filter的注册变为异步，在获取filter之后通知 `render watcher` 更新自己，这样可以利用vue自己的响应式化更新视图，不会阻塞渲染，因此在下初步采用了这个方法。



## 2. 实现

### 2.1 使用根组件的filters

因为filter属于 [asset_types](https://github.com/vuejs/vue/blob/3b43c81216c2e29bd519c447e930d6512b5782e8/src/shared/constants.js#L3) ，关于在Vue实例中asset_types的访问有以下几个结论；具体代码实践可以参考： [Codepen - filter test](https://codepen.io/SHERlocked93/pen/GXmXrM)


1. `asset_types`包括`filters`、`components`、`directives`，以下所有的`asset_types`都自行替换成前面几项
2. 子组件中的`asset_types`访问不到父组件中的`asset_types`，但是可以访问到全局注册的挂载在`$root.$options.asset_types.__proto__`上的`asset_types`，这里对应源码 [src/core/util/options.js](https://github.com/vuejs/vue/blob/3b43c81216c2e29bd519c447e930d6512b5782e8/src/core/util/options.js#L412)
3. 全局注册Vue.asset_types，比如Vue.filters注册的asset_types会挂载到根实例(其他实例的`$root`)的`$options.asset_types.__proto__`上，并被以后所有创建的Vue实例继承，也就是说，以后所有创建的Vue实例都可以访问到
4. 组件的slot的作用域仅限于它被定义的地方，也就是它被定义的组件中，访问不到父组件的`asset_types`，但是可以访问到全局定义的`asset_types`
5. 同理，因为main.js中的`new Vue()`实例是根实例，它中注册的`asset_types`会被挂载在`$root.$options.asset_types`上而不是`$root.$options.asset_types.__proto__`上

因此首先我考虑的是把要注册的filter挂载到根组件上，这样其他组件通过访问`$root`可以拿到注册的filter，这里的实现：

```vue
<template>
  <div>
    {{ rootFilters( sexVal )}}
  </div>
</template>

<script type='text/javascript'>
  import Vue from 'vue'
  import { registerFilters } from 'utils/filters'
  
  export default {
    data() {
      return {
        sexVal: 1  // 性别
      }
    },
    methods: {
      /**
       * 根组件上的过滤器
       * @param id 过滤器ID
       * @param val 传给过滤器的value
       */
      rootFilters(val, id = 'SEX_TYPE') {
        const mth = this.$root.$options.filters[id]
        return mth && mth(val) || val
      }
    },
    created() {
      // 把根组件中的filters响应式化
      Vue.util.defineReactive(this.$root.$options, 'filters', this.$root.$options.filters)
    },
    mounted() {
      registerFilters.call(this)
        .then(data => 
          // 这里获取到数据字典的data
        )
    }
  }
</script>
```

注册filter的js

```js
// utils/filters

import * as Api from 'api'

/**
 * 获取并注册过滤器
 * 注册在$root.$options.filters上不是$root.$options.filters.__proto__上
 * 注意这里的this是vue实例，需要用call或apply调用
 * @returns {Promise}
 */
export function registerFilters() {
  return Api.sysParams()			// 获取数据字典的Api
    .then(({ data }) => {
      Object.keys(data).forEach(T =>
        this.$set(this.$root.$options.filters, T, val => {
          const tar = data[T].find(item => item['paramValue'] === val)
          return tar['paramDesc'] || ''
        })
      )
      return data
    })
    .catch(err => console.error(err, ' in utils/filters.js'))
}
```

这样把根组件上的filters变为响应式化的，并且在渲染的时候因为在`rootFilters`方法中访问了已经在created中被响应式化的`$root.$options.filters`，所以当异步获取的数据被赋给`$root.$options.filters`的时候，会触发这个组件render watcher的重新渲染，这时候再获取`rootFilters`方法的时候就能取到filter了；

那这里为什么不用Vue.filter方法直接注册呢，因为`Object.defineProperty`不能监听`__proto__`上数据的变动，而全局Vue.filter是将过滤器注册在了根组件`$root.$options.asset_types.__proto__`上，因此其变动不能被响应。

这里的代码可以进一步完善，但是这个方法存在一定的问题，首先这里使用了`Vue.util`上不稳定的方法，另外在使用中到处可见`this.$root.$options`这样访问vue实例内部属性的情况，不太文明，读起来也让人困惑。

因此在这个项目做完等待测试的时候我思考了一下，谁说过滤器就一定放在filters里面 -。-，也可以使用mixin来实现嘛

### 2.2 使用mixin

使用mixin要注意一点，因为vue中把data里所有以`_`、`$`开头的变量都作为内部保留的变量，[并不代理到当前实例上](https://github.com/vuejs/vue/blob/3b43c81216c2e29bd519c447e930d6512b5782e8/src/core/instance/state.js#L146)，因此直接`this._xx`是无法访问的，需要通过`this.$data._xx`来访问。

```js
// mixins/sysParamsMixin.js

import * as Api from 'api'

export default {
  data() {
    return {
      _filterFunc: null,       // 过滤器函数
      _sysParams: null,        // 获取数据字典
      _sysParamsPromise: null  // 获取sysParams之后返回的Promise
    }
  },
  methods: {
    /* 注册过滤器到_filterFunc中 */
    _getSysParamsFunc() {
      const thisPromise = this.$data._sysParamsPromise
      return thisPromise || Api.sysParams()			// 获取数据字典的Api
        .then(({ data }) => {
          this.$data._filterFunc = {}
          Object.keys(data).forEach(paramKey =>
            this.$data._filterFunc[paramKey] = val => {		// 过滤器注册到_filterFunc中
              const tar = data[paramKey].find(item => item['paramValue'] === val)
              return tar['paramDesc'] || ''
            })
          return data
        })
        .catch(err => console.error(err, ' in src/mixins/sysParamsMixin.js'))
    },

    /* 按照键值获取单个过滤器 */
    _rootFilters(val, id = 'SEX_TYPE') {
      const func = this.$data._filterFunc
      const mth = func && func[id]
      return mth && mth(val) || val
    },

    /* 获取数据字典 */
    _getSysParams() {
      return this.$data._sysParams
    }
  },
  mounted() {
    this.$data._filterFunc ||
    (this.$data._sysParamsPromise = this._getSysParamsFunc())
  }
}
```

这里把`Api`的promise保存下来，如果其他地方还用到的话直接返回已经是`resolved`状态的promise，就不用再次去请求数据了。

那在我们的组件中怎么使用呢：

```vue
<template>
  <div>
    {{ _rootFilters( sexVal )}}
  </div>
</template>

<script type='text/javascript'>
  import * as Api from 'api'
  import sysParamsMixin from 'mixins/sysParamsMixin'
  
  export default {
    mixins: [sysParamsMixin],
    data() {
      return { sexVal: 1 }
    },
    mounted() {
      this._getSysParamsFunc()
        .then(data => 
          // 这里获取到数据字典的data
        )
    }
  }
</script>
```

这里不仅注册了过滤器，而且也暴露了数据字典，以方便某些地方的列表显示，毕竟这是实际项目中常见的场景。



如果有更好的方法可以讨论一下啊~





---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~


> 参考：
>
> 1. [Vue.js 2.5.17 源码](https://github.com/vuejs/vue)
> 2. [Vue源码阅读系列](https://juejin.im/post/5b38830de51d455888216675)
> 3. [Vue 2.5.17 filter test](https://codepen.io/SHERlocked93/pen/GXmXrM)