<template>
  <div 
    :class="[
      'flex items-center px-4 py-3 cursor-pointer transition-all duration-200 relative group',
      isActive ? 'bg-[#F3F6FA]' : '',
      'hover:bg-[#F9FAFB]',
      agent.status === 0 ? 'opacity-60' : ''
    ]"
    @click="$emit('click')"
  >
    <Avatar 
      :src="agent.avatar" 
      :alt="agent.display_name || agent.name" 
      :fallback-text="(agent.display_name || agent.name).charAt(0).toUpperCase()" 
      class="w-8 h-8 mr-3 text-[11px] rounded-full transition-all duration-200 tracking-[0.5px]"
      :style="getAvatarStyle(agent)"
    />
    <div class="flex-1 min-w-0 flex flex-col justify-center">
      <div class="font-semibold text-sm mb-1 truncate text-[#111827]">
        {{ agent.display_name }}
      </div>
      <div class="text-sm text-[#6B7280] truncate leading-[1.4]">
        {{ agent.description || '暂无描述' }}
      </div>
      <div
        v-if="agent.status === 0"
        class="inline-flex items-center px-2 py-0.5 mt-1 text-[10px] font-medium text-gray-600 bg-gray-100 rounded-full w-fit"
      >
        已禁用
      </div>
    </div>


    <div class="absolute bottom-0 left-4 right-4 h-px bg-[#F0F0F0]"></div>
  </div>
</template>

<script setup>
import Avatar from '@/components/ui/avatar/Avatar.vue';

const props = defineProps({
  agent: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  },
});

const emit = defineEmits(['click']);

const getAvatarStyle = (agent) => {
  if (agent.avatar) return {};
  
  const { backgroundColor, textColor } = generateAvatarColors(agent.display_name || agent.name);
  
  return {
    backgroundColor,
    color: textColor,
    boxShadow: 'inset 0 0 0 1px rgba(0, 0, 0, 0.05)',
    fontWeight: '500'
  };
};

const generateAvatarColors = (name) => {
  const colorPairs = [
    { bg: '#f0f9ff', text: '#0369a1' },
    { bg: '#f0fdf4', text: '#166534' },
    { bg: '#fef2f2', text: '#991b1b' },
    { bg: '#faf5ff', text: '#6b21a8' },
    { bg: '#fff7ed', text: '#9a3412' },
    { bg: '#f8fafc', text: '#475569' },
    { bg: '#fdf4ff', text: '#a21caf' },
    { bg: '#f7fee7', text: '#3f6212' }
  ];
  
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  const colorIndex = Math.abs(hash) % colorPairs.length;
  return {
    backgroundColor: colorPairs[colorIndex].bg,
    textColor: colorPairs[colorIndex].text
  };
};
</script>
