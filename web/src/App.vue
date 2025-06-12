<script setup>
import {onLaunch} from '@dcloudio/uni-app';
import {glyphs} from './static/iconfont/iconfont.json' with {type: 'json'};

const app = getApp();

onLaunch((options) => {
  console.log('onLaunch', options);
  app.globalData.$iconfont = glyphs.reduce((result, item) => {
    result[item.name] = String.fromCharCode(parseInt(item.unicode, 16));
    return result;
  }, {});
})
</script>

<style lang="scss">
/*每个页面公共css */
</style>
