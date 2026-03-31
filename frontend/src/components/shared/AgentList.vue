<template>
  <aside class="w-[265px] border-r border-gray-200 bg-white flex flex-col h-full relative">
    <!-- 头部：标题 + 按钮组 -->
    <header class="px-6 py-4 border-b border-[#F0F0F0] box-border">
      <div class="flex justify-between items-center">
        <h1 class="text-lg font-bold tracking-tight">{{ title }}</h1>
        <div class="flex items-center gap-2">
          <Button 
            v-if="showInitializeButton"
            @click="$emit('initialize')"
            variant="outline"
            size="sm"
            class="text-xs px-2 py-1"
            :disabled="initializeLoading"
          >
            <DownloadIcon class="w-3 h-3 mr-1" />
            {{ initializeLoading ? '初始化中...' : '初始化' }}
          </Button>
          <Button 
            v-if="showCreateButton"
            @click="$emit('create')" 
            size="sm"
            class="text-xs px-2 py-1"
          >
            <PlusIcon class="w-3 h-3 mr-1" />
            创建
          </Button>
        </div>
      </div>
    </header>

    <!-- 搜索区域 -->
    <div v-if="showSearch" class="px-4 py-3 border-b border-[#F0F0F0]">
      <!-- 搜索框 -->
      <div class="relative">
        <SearchIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <Input
          v-model="searchKeyword"
          placeholder="搜索智能体..."
          class="pl-10 text-sm h-8"
          @input="handleSearch"
        />
      </div>
    </div>
    
    <!-- 智能体列表主体 -->
    <main class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent">
      <div v-if="loading" class="flex flex-col items-center justify-center py-10 text-gray-500">
        <div class="w-8 h-8 border-3 border-gray-100 border-t-blue-500 rounded-full animate-spin mb-4"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else class="flex flex-col pb-12">
        <AgentListItem 
          v-for="(agent, index) in filteredAgents" 
          :key="agent.id || agent.name"
          :agent="formatAgentData(agent)"
          :is-active="isAgentActive(agent)"
          @click="handleAgentClick(agent, index)"
        />
        
        <div v-if="filteredAgents.length === 0" class="py-10 text-center text-gray-500 bg-gray-50 rounded-lg mt-4 mx-4 border border-dashed border-gray-300">
          <p>{{ emptyMessage }}</p>
        </div>
      </div>
    </main>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue';
import Button from '@/components/ui/button/Button.vue';
import Input from '@/components/ui/input/Input.vue';
import { PlusIcon, SearchIcon, DownloadIcon } from 'lucide-vue-next';
import AgentListItem from './AgentListItem.vue';

const props = defineProps({
  title: {
    type: String,
    default: '智能体'
  },
  agents: {
    type: Array,
    default: () => []
  },
  activeAgentId: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  // 功能开关
  showSearch: {
    type: Boolean,
    default: false
  },
  showCreateButton: {
    type: Boolean,
    default: false
  },
  showInitializeButton: {
    type: Boolean,
    default: false
  },
  initializeLoading: {
    type: Boolean,
    default: false
  },
  emptyMessage: {
    type: String,
    default: '暂无可用智能体'
  }
});

const emit = defineEmits([
  'agent-select', 
  'create',
  'initialize'
]);

// 搜索状态
const searchKeyword = ref('');

// 计算过滤后的智能体列表
const filteredAgents = computed(() => {
  let filtered = props.agents;

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase();
    filtered = filtered.filter(agent => {
      const name = agent.agent_name || agent.display_name || agent.name || '';
      const code = agent.agent_code || agent.name || '';
      const description = agent.description || '';
      
      return name.toLowerCase().includes(keyword) ||
             code.toLowerCase().includes(keyword) ||
             description.toLowerCase().includes(keyword);
    });
  }

  return filtered;
});

// 判断智能体是否处于活动状态
const isAgentActive = (agent) => {
  const agentId = agent.agent_code || agent.name;
  return agentId === props.activeAgentId;
};

// 格式化智能体数据，统一不同页面的数据结构
const formatAgentData = (agent) => {
  return {
    id: agent.id,
    name: agent.agent_code || agent.name,
    display_name: agent.agent_name || agent.display_name || agent.name,
    description: agent.description || '',
    model: agent.model_name || agent.model || 'deepseek-reasoner-vze8',
    status: agent.status,
    display_order: agent.display_order,
    avatar: agent.avatar,
    color: agent.color || generateColorFromName(agent.agent_name || agent.name)
  };
};

// 根据名称生成颜色
const generateColorFromName = (name) => {
  if (!name) return '#5c6bc0';
  
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  const colors = [
    '#5c6bc0', '#26a69a', '#ec407a', '#ab47bc',
    '#ef5350', '#ffa726', '#ffee58', '#66bb6a'
  ];
  
  return colors[Math.abs(hash) % colors.length];
};

// 事件处理
const handleSearch = () => {
  // 搜索逻辑已通过计算属性实现
};


const handleAgentClick = (agent, index) => {
  emit('agent-select', agent, index);
};
</script>
