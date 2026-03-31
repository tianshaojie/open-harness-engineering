<template>
  <div
    :class="[
      'flex items-center rounded-full bg-[#232336] px-4 py-2 relative shadow-md w-full voice-recorder-bar', 
      isMobile ? 'voice-recorder-bar-mobile' : '',
      uploading && isMobile ? 'uploading' : ''
    ]"
    style="min-height:48px;"
  >
    <button
      class="w-10 h-10 flex items-center justify-center rounded-full bg-[#282848] text-[#8ca2f7] mr-2 voice-recorder-btn"
      @click="handleCancel"
      :disabled="uploading"
    >
      <X class="w-6 h-6" />
    </button>
    <!-- 右侧信号流动点块心电图区域 -->
    <div class="flex-1 flex items-center justify-center overflow-hidden">
      <div
        class="relative flex items-center justify-center w-full h-8 voice-recorder-wave"
        :class="isMobile ? 'h-6' : ''"
        style="position: relative;"
      >
        <div
          v-for="(point, i) in waveArray"
          :key="i"
          :style="{
            width: uploading && isMobile ? '6px' : (isMobile ? '4px' : '4px'),
            height: point + 'px',
            background: i === waveArray.length - 1 ? '#a5b4fc' : '#8ca2f7',
            borderRadius: uploading && isMobile ? '3px' : (isMobile ? '2px' : '2px'),
            position: 'absolute',
            left: (i / (waveArray.length - 1)) * 100 + '%',
            top: '50%',
            transform: 'translate(-50%, -50%)',
            transition: 'all 0.12s cubic-bezier(.4,0,.2,1)',
            opacity: 0.6 + 0.4 * (point / (props.isMobile ? maxHeightMobile : maxHeight))
          }"
        ></div>
      </div>
    </div>
    <span class="ml-2 text-[#8ca2f7] text-sm min-w-[40px] voice-recorder-time" :class="isMobile ? 'text-xs ml-1' : ''">{{ formattedTime }}</span>
    <button
      class="w-10 h-10 flex items-center justify-center rounded-full bg-[#6c63ff] text-white ml-2 voice-recorder-btn"
      @click="handleConfirm"
      :disabled="uploading"
    >
      <Loader2 v-if="uploading" class="w-6 h-6 animate-spin" />
      <Check v-else class="w-6 h-6" />
    </button>
  </div>
  <!-- 移除报错提示div -->
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { X, Check, Loader2 } from 'lucide-vue-next';

const props = defineProps({
  uploading: Boolean,
  isMobile: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['cancel', 'confirm', 'result']);

const WAVE_COUNT_DESKTOP = 60;
const WAVE_COUNT_MOBILE = 30;
const maxHeight = 22;
const minHeight = 3;
const maxHeightMobile = 20; // 移动端最大高度稍小
const waveArray = ref(Array(WAVE_COUNT_DESKTOP).fill(minHeight));
// 移除 wavePath computed
let waveAnimTimer = null;
let audioContext = null;
let analyser = null;
let sourceNode = null;
let dataArray = null;
let streamRef = null;
let lastRms = 4;

function updateWaveArrayCount() {
  // 上传状态下减少音频点数量，确保有足够空间
  let count;
  if (props.uploading && props.isMobile) {
    count = 30; // 上传时移动端显示30个点
  } else {
    count = props.isMobile ? WAVE_COUNT_MOBILE : WAVE_COUNT_DESKTOP;
  }
  
  if (waveArray.value.length !== count) {
    waveArray.value = Array(count).fill(minHeight);
  }
}

watch(() => props.isMobile, updateWaveArrayCount, { immediate: true });
watch(() => props.uploading, updateWaveArrayCount, { immediate: true });

function startWaveAnim() {
  updateWaveArrayCount();
  const interval = props.isMobile ? 120 : 100; // 移动端和PC端都降低更新频率
  if (!analyser) {
    waveAnimTimer = setInterval(() => {
      // 随机信号流动，无衰减
      const currentMaxHeight = props.isMobile ? maxHeightMobile : maxHeight;
      let next = minHeight + Math.floor(Math.random() * (currentMaxHeight - minHeight));
      let arr = waveArray.value.slice(1);
      arr.push(next);
      waveArray.value = arr;
    }, interval);
    return;
  }
  waveAnimTimer = setInterval(() => {
    analyser.getByteTimeDomainData(dataArray);
    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {
      const v = dataArray[i] - 128;
      sum += v * v;
    }
    let rms = Math.sqrt(sum / dataArray.length);
    rms = lastRms * 0.7 + rms * 0.3;
    lastRms = rms;
    // 信号强度，右侧点块更大
    const currentMaxHeight = props.isMobile ? maxHeightMobile : maxHeight;
    let next = Math.max(minHeight, Math.min(currentMaxHeight, rms * 0.7 + minHeight));
    let arr = waveArray.value.slice(1);
    arr.push(next);
    waveArray.value = arr;
  }, interval);
}
function stopWaveAnim() {
  if (waveAnimTimer) {
    clearInterval(waveAnimTimer);
    waveAnimTimer = null;
  }
  waveArray.value = Array(WAVE_COUNT_DESKTOP).fill(minHeight);
  lastRms = 4;
}

const recordingTime = ref(0);
const recordingTimer = ref(null);
const formattedTime = computed(() => {
  const min = Math.floor(recordingTime.value / 60).toString();
  const sec = (recordingTime.value % 60).toString().padStart(2, '0');
  return `${min}:${sec}`;
});

const error = ref('');

// 录音相关
const audioChunks = ref([]);
const mediaRecorder = ref(null);
let stopped = false; // 防止多次 stop/emit

async function startRecording() {
  error.value = '';
  stopped = false;
  if (!navigator.mediaDevices || !window.MediaRecorder) {
    error.value = '当前浏览器不支持录音';
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef = stream;
    // 检查支持的格式，优先ogg
    let mimeType = '';
    if (window.MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
      mimeType = 'audio/ogg;codecs=opus';
    } else if (window.MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
      mimeType = 'audio/webm;codecs=opus';
    } else {
      mimeType = '';
    }
    
    mediaRecorder.value = mimeType
      ? new window.MediaRecorder(stream, { mimeType })
      : new window.MediaRecorder(stream);
    audioChunks.value = [];
    mediaRecorder.value.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunks.value.push(e.data);
    };
    mediaRecorder.value.onstop = () => {
      stream.getTracks().forEach(track => track.stop());
      // 导出音频文件
      const mimeType = mediaRecorder.value && mediaRecorder.value.mimeType ? mediaRecorder.value.mimeType : 'audio/ogg';
      const ext = mimeType.includes('ogg') ? 'ogg' : 'webm';
      const audioBlob = new Blob(audioChunks.value, { type: mimeType });
      const file = new File([audioBlob], `record.${ext}`, { type: mimeType });
      emit('result', file);
    };
    // Web Audio API 实时分析
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 128;
    dataArray = new Uint8Array(analyser.fftSize);
    sourceNode = audioContext.createMediaStreamSource(stream);
    sourceNode.connect(analyser);
    mediaRecorder.value.start();
    recordingTime.value = 0;
    recordingTimer.value = setInterval(() => recordingTime.value++, 1000);
    startWaveAnim();
  } catch (e) {
    error.value = '无法获取麦克风权限';
  }
}

function stopRecording() {
  if (stopped) return;
  stopped = true;
  if (mediaRecorder.value) {
    mediaRecorder.value.stop();
  }
  clearInterval(recordingTimer.value);
  stopWaveAnim();
  // 释放 Web Audio 资源
  if (audioContext) {
    audioContext.close();
    audioContext = null;
    analyser = null;
    sourceNode = null;
    dataArray = null;
  }
  if (streamRef) {
    streamRef = null;
  }
}

function handleCancel() {
  stopRecording();
  emit('cancel');
}

function handleConfirm() {
  if (stopped) return;
  stopRecording();
  emit('confirm');
  // 不在这里导出文件，等 onstop 事件
}

onMounted(() => {
  startRecording();
});
onUnmounted(() => {
  stopRecording();
});

defineExpose({ stopRecording });
</script>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
@media (max-width: 768px) {
.voice-recorder-bar {
  min-height: 36px !important;
  padding-left: 10px !important;
  padding-right: 10px !important;
  border-radius: 24px !important;
}
.voice-recorder-btn {
  width: 32px !important;
  height: 32px !important;
}
.voice-recorder-wave {
  height: 24px !important;
  padding: 0 8px !important;
}

/* PC端音频点间距优化 */
.voice-recorder-bar:not(.voice-recorder-bar-mobile) .voice-recorder-wave {
  padding: 0 16px !important;
}

.voice-recorder-bar:not(.voice-recorder-bar-mobile) .voice-recorder-wave > div {
  margin: 0 1px !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}
.voice-recorder-time {
  font-size: 12px !important;
  margin-left: 4px !important;
  min-width: 28px !important;
}
.voice-recorder-bar-mobile {
  position: fixed !important;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw !important;
  border-radius: 24px !important;
  z-index: 9999;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.08);
  border-top: 1px solid #232336;
  background: #232336 !important;
  min-height: 64px !important;
  height: 64px !important;
  display: flex;
  align-items: center;
  padding-bottom: env(safe-area-inset-bottom, 16px) !important;
  padding-top: 0 !important;
}

/* 移动端上传状态布局优化 */
.voice-recorder-bar-mobile.uploading {
  padding-left: 8px !important;
  padding-right: 8px !important;
}

.voice-recorder-bar-mobile.uploading .voice-recorder-btn {
  width: 32px !important;
  height: 32px !important;
  margin: 0 2px !important;
}

.voice-recorder-bar-mobile.uploading .voice-recorder-time {
  min-width: 28px !important;
  margin-left: 4px !important;
  margin-right: 4px !important;
  font-size: 11px !important;
}

/* 移动端音频点间距优化 */
.voice-recorder-bar-mobile .voice-recorder-wave {
  gap: 3px !important;
  padding: 0 12px !important;
}

.voice-recorder-bar-mobile .voice-recorder-wave > div {
  margin: 0 1px !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

/* 移动端上传状态音频点优化 */
.voice-recorder-bar-mobile.uploading .voice-recorder-wave {
  padding: 0 16px !important;
}

.voice-recorder-bar-mobile.uploading .voice-recorder-wave > div {
  width: 6px !important;
  border-radius: 3px !important;
  margin: 0 3px !important;
  min-height: 4px !important;
}
}
</style> 