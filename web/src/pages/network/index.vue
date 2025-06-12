<template>
<!--  #ifndef H5-->
  <uni-nav-bar left-icon="left" title="网络设置"/>
<!--  #endif-->
  <view class="container">
    <view class="title">
      附近WIFI列表
    </view>
    <uni-list class="wifi-list">
      <template v-for="(item, index) in wifiList" :key="index" >
        <uni-list-item direction="column" class="wifi-item" :class="{'active': activeWifi === item.ssid }">
          <template v-slot:header>
            <view class="wifi-name">
              <view class="name">{{item.ssid}}</view>
              <view class="logo">
                <view class="lock-logo">
                  <uni-icons class="locked-logo" color="#ccc" fontFamily="CustomFont" :size="26" v-if="item.needPwd">
                    {{ app.globalData.$iconfont['lock'] }}
                  </uni-icons>
                  <uni-icons class="unlock-logo" color="#66ccff" fontFamily="CustomFont" :size="26" v-else>
                    {{ app.globalData.$iconfont['unlock'] }}
                  </uni-icons>
                </view>
                <view class="wifi-signal">
                  <uni-icons class="wifi-1-logo" color="#66ccff" fontFamily="CustomFont" :size="26" v-if="item.signal >= 66">
                    {{ app.globalData.$iconfont['wifi-3'] }}
                  </uni-icons>

                  <uni-icons class="wifi-2-logo" color="#66ccff" fontFamily="CustomFont" :size="26" v-else-if="item.signal >= 33">
                    {{ app.globalData.$iconfont['wifi-2'] }}
                  </uni-icons>

                  <uni-icons class="wifi-3-logo" color="#66ccff" fontFamily="CustomFont" :size="26" v-else>
                    {{ app.globalData.$iconfont['wifi-1'] }}
                  </uni-icons>
              </view>
                <view class="connect-logo">
                  <uni-icons class="connected-logo" color="#39c5bb" fontFamily="CustomFont" :size="26" v-if="activeWifi === item.ssid">
                    {{ app.globalData.$iconfont['connected'] }}
                  </uni-icons>
                  <uni-icons class="unconnect-logo" color="#ccc" fontFamily="CustomFont" :size="18" v-else>
                    {{ app.globalData.$iconfont['unconnect'] }}
                  </uni-icons>
                </view>
              </view>
            </view>
          </template>
          <template v-slot:body>
            <view class="operate">
              <button class="mini-btn" type="primary" plain="true" :disabled="activeWifi === item.ssid">连接</button>
            </view>
          </template>
        </uni-list-item>
      </template>
    </uni-list>
  </view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app';
import { ref } from 'vue';

const wifiList = ref([]);
const activeWifi = ref(null);

const app = getApp();

onLoad((options) => {
  activeWifi.value = 'wifiName';
  setWifiList();
})

function setWifiList() {
  const data = [
    {
      ssid: 'wifiName3',
      needPwd: true,
      signal: 60,
    },
    {
      ssid: 'wifiName3',
      needPwd: true,
      signal: 60,
    },
    {
      ssid: 'wifiName',
      needPwd: false,
      signal: 100,
    },
    {
      ssid: 'wifiName2',
      needPwd: true,
      signal: 30,
    },
    {
      ssid: 'wifiName2',
      needPwd: true,
      signal: 30,
    },
    {
      ssid: 'wifiName2',
      needPwd: true,
      signal: 30,
    }
  ];
  data.forEach((item) => {
    wifiList.value.push({
      ssid: item.ssid,
      needPwd: item.needPwd,
      signal: item.signal,
    })
  })
}

</script>

<style scoped lang="scss">
.title {
  font-weight: bold;
  text-align: center;
  margin: 1rem 0;
}

.wifi-item:nth-child(2n) {
  background-color: #eeebeb !important;
}
.wifi-item:nth-child(2n+1) {
  background-color: #fff!important;
}
.wifi-item {
  display: flex;
  flex-flow: row;
}
.wifi-item.active {
  background-color: #d5efda !important;
}
.wifi-name {
  display: flex;
  align-items: center;
  gap: 1rem;
  .logo {
    display: flex;
  }
}
.wifi-body {
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 1rem;
}
.operate {
  width: 4rem;
  button {
    font-size: 14px;
  }
}
</style>