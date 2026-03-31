<template>
  <div v-if="hasDataSource" class="p-2 bg-white rounded-lg border border-gray-200 h-full flex flex-col">
    
    <!-- 优先使用userData，显示所有图表类型（包含饼图） -->
    <template v-if="userData && userData.length > 0 && columns && columns.length > 0">
      <!-- 图表控制面板 -->
      <div class="mb-3 p-2 bg-white rounded-lg border border-gray-200 flex-shrink-0">
        <div class="flex flex-wrap gap-3 items-center">
          <!-- 图表类型选择 -->
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-black w-16">图表类型:</span>
                <div class="flex bg-white rounded-md p-1 border border-gray-200">
                  <button
                    v-for="(chartType, index) in getAvailableChartTypes()"
                    :key="index"
                    @click="selectChartType(index)"
                    :class="[
                      'px-3 py-1 text-xs rounded transition-colors',
                      selectedChartType === index
                        ? 'bg-black text-white'
                        : 'text-black hover:bg-gray-100'
                    ]"
                  >
                    {{ chartType }}
                  </button>
                </div>
          </div>

          <!-- X轴选择（黑白主题Select） -->
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-black w-12">X轴:</span>
            <Select v-model="selectedXAxis" class="w-auto">
              <SelectTrigger
                class="bg-white text-black border border-gray-300 focus:ring-0 focus:outline-none h-8 text-xs !w-auto w-max max-w-none"
              >
                <SelectValue class="whitespace-nowrap truncate" />
              </SelectTrigger>
              <SelectContent
                class="bg-white text-black border border-gray-300 !w-[max-content] !min-w-max !max-w-none"
                :style="{ width: 'max-content', minWidth: 'max-content', maxWidth: 'none' }"
              >
                <SelectItem v-for="(col, index) in columns" :key="index" :value="col" class="text-xs">
                  {{ col }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- 左Y轴选择 -->
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-black w-20">左Y轴:</span>
            <Select v-model="selectedLeftYAxis" class="w-auto">
              <SelectTrigger class="bg-white text-black border border-gray-300 focus:ring-0 focus:outline-none h-8 text-xs">
                <SelectValue class="whitespace-nowrap truncate">{{ getLeftYAxisDisplayValue }}</SelectValue>
              </SelectTrigger>
              <SelectContent
                class="bg-white text-black border border-gray-300 !w-[max-content] !min-w-max !max-w-none"
                :style="{ width: 'max-content', minWidth: 'max-content', maxWidth: 'none' }"
              >
                <SelectItem value="__none__" class="text-xs text-gray-500">
                  未选择
                </SelectItem>
                <SelectItem v-for="(col, index) in columns" :key="index" :value="col" class="text-xs">
                  {{ col }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- 右Y轴选择 -->
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-black w-20">右Y轴:</span>
            <Select v-model="selectedRightYAxis">
              <SelectTrigger class="bg-white text-black border border-gray-300 focus:ring-0 focus:outline-none h-8 text-xs min-w-[120px]">
                <SelectValue>{{ getRightYAxisDisplayValue }}</SelectValue>
              </SelectTrigger>
              <SelectContent class="bg-white text-black border border-gray-300">
                <SelectItem value="__none__" class="text-xs text-gray-500">
                  未选择
                </SelectItem>
                <SelectItem v-for="(col, index) in columns" :key="index" :value="col" class="text-xs">
                  {{ col }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      <!-- 图表展示区域 -->
      <div :class="chartContainerClasses">
        <div 
          :class="chartContentClasses"
          :ref="(el) => setChartContainer(el, 0)"
        ></div>
        <!-- X轴名称显示在图表下方居中（仅柱状图和折线图显示） -->
        <div v-if="selectedXAxis && !isPieChart(0)" class="text-center text-xs font-medium text-gray-600 flex-shrink-0">
          {{ selectedXAxis }}
        </div>
      </div>
    </template>

    <!-- 当没有userData时，显示chartSuggestions -->
    <template v-else-if="chartSuggestions && chartSuggestions.length > 0">
    <!-- 当只有一个图表方案时，只显示文字标题 -->
    <div v-if="!hasMultipleCharts" :class="[
      'flex-shrink-0',
      studioMode ? 'mb-1.5 px-2 pt-2' : 'mb-3'
    ]">
      <h4 class="text-sm font-medium text-gray-700">{{ getChartTypeName(chartSuggestions[0]) || '图表方案 1' }}</h4>
    </div>

    <!-- 当有多个图表方案时，显示完整的tabs组件 -->
    <Tabs v-else v-model="activeKey" class="w-full h-full flex flex-col" @update:model-value="handleTabChange">
      <TabsList class="inline-flex items-center justify-start bg-gray-200 mb-1.5 h-auto p-0.5 w-auto">
        <TabsTrigger 
          v-for="(chart, index) in chartSuggestions" 
          :key="index.toString()" 
          :value="index.toString()"
          class="px-3 py-1.5 text-xs"
        >
          {{ getChartTypeName(chart) || `图表 ${index + 1}` }}
        </TabsTrigger>
      </TabsList>
      
      <TabsContent
        v-for="(chart, index) in chartSuggestions"
        :key="index.toString()"
        :value="index.toString()"
        class="mt-0 flex-1 min-h-0 flex flex-col"
      >
        <div :class="[
          'text-sm text-gray-600 flex-shrink-0',
          studioMode ? 'mb-2 px-2 pt-2' : 'mb-2 px-1'
        ]">{{ chart.suggest_reason || '图表方案' }}</div>
        <div class="flex flex-col flex-1 min-h-0">
          <div :class="[
            'w-full my-3 bg-white rounded-md p-3 transition-opacity duration-300',
            studioMode ? 'flex-1 min-h-[300px]' : 'min-h-[300px]'
          ]"
          :ref="(el) => setChartContainer(el, index)"
        ></div>
          <!-- X轴名称显示在图表下方居中（仅柱状图和折线图显示） -->
          <div v-if="getXAxisNameForChart(index) && !isPieChart(index)" class="text-center text-xs font-medium text-gray-600">
            {{ getXAxisNameForChart(index) }}
          </div>
        </div>
      </TabsContent>
    </Tabs>

    <!-- 当只有一个图表方案时，直接显示图表内容 -->
    <div v-if="!hasMultipleCharts" class="flex-1 min-h-0 flex flex-col">
      <div :class="[
        'text-sm text-gray-600 flex-shrink-0',
        studioMode ? 'mb-2 px-2 pt-2' : 'mb-2 px-1'
      ]">{{ chartSuggestions[0]?.suggest_reason || '图表方案' }}</div>
      <div class="flex flex-col flex-1 min-h-0">
        <div :class="[
          'w-full my-3 bg-white rounded-md p-3 transition-opacity duration-300',
          studioMode ? 'flex-1 min-h-[300px]' : 'min-h-[300px]'
        ]"
        :ref="(el) => setChartContainer(el, 0)"
        ></div>
        <!-- X轴名称显示在图表下方居中（仅柱状图和折线图显示） -->
        <div v-if="getXAxisNameForChart(0) && !isPieChart(0)" class="text-center text-xs font-medium text-gray-600">
          {{ getXAxisNameForChart(0) }}
        </div>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup lang="ts">
// {{CHENGQI:
// Action: Modified
// Reason: 添加onActivated导入，用于监听组件激活事件
// Principle_Applied: 单一职责原则 - 明确导入所需的Vue生命周期钩子
// }}
import { ref, computed, onMounted, onUnmounted, onActivated, watch, onUpdated, nextTick, ComponentPublicInstance } from 'vue';
import * as echarts from 'echarts';
import eventBus, { EventTypes } from '@/utils/eventBus';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { getChartOption } from '@/views/my-dashboard/utils/chartConfig';
// 图表类型常量
const CHART_TYPES = {
  TYPES: ['line', 'bar', 'pie'],
  TITLES: ['折线图', '柱状图', '饼图']
};

// 图表类型到 displayType 的映射（仪表盘配置）
const CHART_TYPE_TO_DISPLAY_TYPE: Record<string, number> = {
  'line': 2,  // 折线图
  'bar': 3,   // 柱状图
  'pie': 4    // 饼图
};

// 获取可用的图表类型（根据数据量决定是否显示图表）
const getAvailableChartTypes = () => {
  // 检查数据量
  const dataLength = props.userData?.length || 0;
  
  // 1条数据：不显示图表
  if (dataLength <= 1) {
    return [];
  }
  
  // 2～10条数据：饼图、折线图、柱状图
  if (dataLength >= 2 && dataLength <= 10) {
    return ['折线图', '柱状图', '饼图'];
  }
  
  // >10条数据：只展示折线图、柱状图
  if (dataLength > 10) {
    return ['折线图', '柱状图'];
  }
  
  return [];
};

// 配置常量
// {{CHENGQI:
// Action: Modified
// Reason: 提高MIN_VALID_WIDTH阈值，更有效地检测智能体切换时的容器宽度异常
// Principle_Applied: 防御性编程 - 设置合理的阈值确保图表有足够显示空间
// Optimization: 配合onActivated方案，提供更准确的异常检测
// }}
const CONFIG = {
  // 尺寸相关
  DEFAULT_HEIGHT: 300,            // 默认图表高度
  MIN_VALID_WIDTH: 200,          // 最小有效容器宽度，设置为200px以检测100px的异常宽度
  
  // 时间相关
  DEBOUNCE_DELAY: 200,            // 防抖延迟(ms)
  RESIZE_DEBOUNCE_DELAY: 100,     // 调整大小防抖延迟(ms)
  CHECK_DELAY: 100,               // 检查延迟(ms)
  
  // 重试相关
  MAX_RETRY_COUNT: 3              // 最大重试次数
};

/**
 * 防抖函数 - 限制函数在一定时间内只执行一次
 * @param fn 需要防抖的函数
 * @param delay 延迟时间，单位毫秒
 * @returns 防抖处理后的函数
 */
function debounce<T extends (...args: any[]) => any>(fn: T, delay: number): (...args: Parameters<T>) => void {
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

// 辅助函数：触发滚动到底部事件
const triggerScrollToBottom = debounce(() => {
  eventBus.emit(EventTypes.CONTENT_RENDERED, {
    type: 'visualization',
    contentLength: 1000, // 图表内容比较大
    isFirstRender: true
  });
}, CONFIG.DEBOUNCE_DELAY);

// 本地图表配置映射
const chartConfigMap = {
  // 折线图配置
  line: {
    title: {
      show: false
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    grid: {
      left: '6%',
      right: '8%',
      bottom: 30, // 为旋转45度的x轴标签留出空间
      top: '15%',
      height: '75%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      axisLabel: {
        fontSize: 10,
        rotate: 45,
        interval: 'auto', // 自动计算间隔，避免标签重叠
        formatter: function(value: string) {
          // 时间格式化，精确到秒级
          if (value && typeof value === 'string') {
            // 尝试解析为时间格式
            const date = new Date(value);
            if (!isNaN(date.getTime())) {
              return date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
              });
            }
          }
          // 如果不是时间格式，进行截断
          if (value.length > 12) {
            return value.substring(0, 12) + '...';
          }
          return value;
        }
      }
    },
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            type: 'dashed',
            color: '#e0e0e0'
          }
        },
        axisLine: {
          show: false
        }
      }
    ],
    series: [
      {
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 3
        },
        itemStyle: {
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'top',
          fontSize: 10,
          color: '#333'
        }
      }
    ]
  },
  
  // 柱状图配置
  bar: {
    title: {
      show: false
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '6%',
      right: '8%',
      bottom: 30, // 为旋转45度的x轴标签留出空间
      top: '15%',
      height: '75%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      axisLabel: {
        fontSize: 10,
        rotate: 45,
        interval: 'auto', // 自动计算间隔，避免标签重叠
        margin: 15, // 增加标签与坐标轴的距离，便于区分
        formatter: function(value: string) {
          // 时间格式化，精确到秒级
          if (value && typeof value === 'string') {
            // 尝试解析为时间格式
            const date = new Date(value);
            if (!isNaN(date.getTime())) {
              return date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
              });
            }
          }
          // 如果不是时间格式，进行截断
          if (value.length > 12) {
            return value.substring(0, 12) + '...';
          }
          return value;
        }
      }
    },
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            type: 'dashed',
            color: '#e0e0e0'
          }
        },
        axisLine: {
          show: false
        }
      }
    ],
    series: [
      {
        type: 'bar',
        itemStyle: {
          borderRadius: [4, 4, 0, 0]
        },
        label: {
          show: false,
          position: 'top',
          fontSize: 10,
          color: '#333'
        }
      }
    ]
  },
  
  // 饼图配置
  pie: {
    title: {
      text: '数据占比',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: {
        fontSize: 12
      }
    },
    series: [
      {
        type: 'pie',
        radius: '50%',
        center: ['50%', '60%'],
        data: [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  },
  
  // 散点图配置
  scatter: {
    title: {
      text: '数据分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item'
    },
    grid: {
      left: '2%',
      right: '6%',
      bottom: 20,
      top: '15%',
      height: '75%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: {
        fontSize: 12
      }
    },
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            type: 'dashed',
            color: '#e0e0e0'
          }
        },
        axisLine: {
          show: false
        }
      }
    ],
    series: [
      {
        type: 'scatter',
        symbolSize: 8
      }
    ]
  }
};

// 根据图表类型和数据生成配置
const generateChartConfig = (chartType: string, data: any[], chartTitle?: string) => {
  const baseConfig = chartConfigMap[chartType as keyof typeof chartConfigMap];
  if (!baseConfig) {
    return null;
  }

  // 深拷贝基础配置
  const config = JSON.parse(JSON.stringify(baseConfig));
  
  // 设置标题
  if (chartTitle) {
    config.title.text = chartTitle;
  }
  
  // 设置图例
  if (chartType === 'line' || chartType === 'bar') {
    config.legend = {
      data: [selectedLeftYAxis.value, selectedRightYAxis.value].filter(value => value && value !== '__none__'),
      top: 5,
      type: 'scroll',
      textStyle: {
        color: '#333',
        fontSize: 12
      },
      icon: 'rect',
      itemWidth: 18,
      itemHeight: 10,
      pageButtonItemGap: 5,
      pageButtonGap: 5,
      pageButtonPosition: 'end',
      pageIconColor: '#333',
      pageIconInactiveColor: '#bbb',
      pageIconSize: 12,
      pageTextStyle: {
        color: '#333'
      }
    };
  }
  
  // 根据数据类型设置配置
  if (data && data.length > 0) {
    const firstRow = data[0];
    const columns = Object.keys(firstRow);
    
    if (chartType === 'line' || chartType === 'bar') {
      // 折线图和柱状图：使用选中的X轴和左右双Y轴
      // 检查是否有有效的Y轴选择
      const hasValidLeftYAxis = selectedLeftYAxis.value && selectedLeftYAxis.value !== '__none__';
      const hasValidRightYAxis = selectedRightYAxis.value && selectedRightYAxis.value !== '__none__';
      
      if (selectedXAxis.value && (hasValidLeftYAxis || hasValidRightYAxis)) {
        // 设置X轴数据（横坐标）
        config.xAxis.data = data.map(row => row[selectedXAxis.value]);
        
        // 移除X轴名称配置，名称将在图表容器外部单独显示
        // 增加 axisLabel margin，便于区分
        if (config.xAxis.axisLabel) {
          config.xAxis.axisLabel.margin = 15;
        } else {
          config.xAxis.axisLabel = { margin: 15 };
        }
        
        // 设置左右双Y轴
        config.yAxis = [
          ...(hasValidLeftYAxis ? [{
            type: 'value',
            name: selectedLeftYAxis.value,
            nameLocation: 'end',
            nameGap: 10,
            nameTextStyle: {
              color: '#333',
              fontSize: 12
            },
            axisLabel: {
              fontSize: 12,
              color: '#ee6666'
            },
            axisLine: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                type: 'dashed',
                color: '#e0e0e0'
              }
            }
          }] : []),
          ...(hasValidRightYAxis ? [{
            type: 'value',
            name: selectedRightYAxis.value,
            nameLocation: 'end',
            nameGap: 10,
            nameTextStyle: {
              color: '#333',
              fontSize: 12
            },
            axisLabel: {
              fontSize: 12,
              color: '#5470c6'
            },
            axisLine: {
              show: false
            },
            splitLine: {
              show: false
            }
          }] : [])
        ];
        
        // 设置图例数据
        config.legend.data = [selectedLeftYAxis.value, selectedRightYAxis.value].filter(value => value && value !== '__none__');
        
        // 创建两个系列（左Y轴和右Y轴）
        config.series = [];
        
        // 添加左Y轴系列
        if (hasValidLeftYAxis) {
          config.series.push({
            type: chartType,
            name: selectedLeftYAxis.value,
            yAxisIndex: 0, // 使用左Y轴
            data: data.map(row => {
              const value = row[selectedLeftYAxis.value];
              return typeof value === 'number' ? value : parseFloat(value) || 0;
            }),
            smooth: chartType === 'line',
            itemStyle: {
              borderWidth: 2,
              color: '#ee6666'
            },
            lineStyle: {
              width: 3,
              color: '#ee6666'
            }
          });
        }
        
        // 添加右Y轴系列
        if (hasValidRightYAxis) {
          config.series.push({
            type: chartType,
            name: selectedRightYAxis.value,
            yAxisIndex: hasValidLeftYAxis ? 1 : 0, // 如果左Y轴为空，右Y轴使用索引0
            data: data.map(row => {
              const value = row[selectedRightYAxis.value];
              return typeof value === 'number' ? value : parseFloat(value) || 0;
            }),
            smooth: chartType === 'line',
            itemStyle: {
              borderWidth: 2,
              color: '#5470c6'
            },
            lineStyle: {
              width: 3,
              color: '#5470c6'
            }
          });
        }
        
        // 添加dataZoom配置 - 默认显示100%数据
        config.dataZoom = [
          {
            type: 'slider',
            show: true,
            xAxisIndex: [0],
            start: 0, // 默认显示100%的数据
            end: 100,
            height: 20,
            bottom: 5,
            borderColor: 'transparent',
            backgroundColor: '#f5f5f5',
            fillerColor: 'rgba(167,183,204,0.4)',
            handleStyle: {
              color: '#fff',
              shadowBlur: 3,
              shadowColor: 'rgba(0,0,0,0.6)',
              shadowOffsetX: 2,
              shadowOffsetY: 2
            },
            textStyle: {
              color: '#333'
            }
          },
          {
            type: 'inside',
            xAxisIndex: [0],
            start: 0,
            end: 100
          }
        ];
      }
    } else if (chartType === 'pie') {
      // 饼图：使用前两列，第一列作为名称，第二列作为数值
      if (columns.length >= 2) {
        // 使用所有数据进行展示
        const pieData = data.map(row => ({
          name: row[columns[0]],
          value: typeof row[columns[1]] === 'number' ? row[columns[1]] : parseFloat(row[columns[1]]) || 0
        }));
        
        config.series[0].data = pieData;
      }
    } else if (chartType === 'scatter') {
      // 散点图：使用前两列作为X和Y轴
      if (columns.length >= 2) {
        config.series[0].data = data.map(row => [
          typeof row[columns[0]] === 'number' ? row[columns[0]] : parseFloat(row[columns[0]]) || 0,
          typeof row[columns[1]] === 'number' ? row[columns[1]] : parseFloat(row[columns[1]]) || 0
        ]);
        
        // 移除X轴名称配置，名称将在图表容器外部单独显示
        // 增加 axisLabel margin，便于区分
        if (config.xAxis.axisLabel) {
          config.xAxis.axisLabel.margin = 15;
        } else {
          config.xAxis.axisLabel = { margin: 15 };
        }
        
        config.yAxis.name = columns[1];
        config.yAxis.nameLocation = 'end';
        config.yAxis.nameGap = 10;
        config.yAxis.nameTextStyle = {
          color: '#333',
          fontSize: 12
        };
      }
    }
  }
  
  // 恢复ECharts默认浅色风格
  delete config.backgroundColor;
  
  // 只为有坐标轴的图表类型清理坐标轴样式
  if (chartType === 'line' || chartType === 'bar' || chartType === 'scatter') {
    if (config.xAxis?.axisLabel) delete config.xAxis.axisLabel.color;
    if (config.xAxis?.axisLine) delete config.xAxis.axisLine;
    if (config.xAxis?.splitLine) delete config.xAxis.splitLine;
    if (config.yAxis?.axisLabel) delete config.yAxis.axisLabel.color;
    if (config.yAxis?.axisLine) delete config.yAxis.axisLine;
    if (config.yAxis?.splitLine) delete config.yAxis.splitLine;
  }
  
  return config;
};

// 根据图表标题推断图表类型
const inferChartType = (title: string): string => {
  const lowerTitle = title.toLowerCase();
  
  if (lowerTitle.includes('趋势') || lowerTitle.includes('变化') || lowerTitle.includes('增长')) {
    return 'line';
  }
  if (lowerTitle.includes('对比') || lowerTitle.includes('比较') || lowerTitle.includes('排名')) {
    return 'bar';
  }
  if (lowerTitle.includes('占比') || lowerTitle.includes('分布') || lowerTitle.includes('比例')) {
    return 'pie';
  }
  if (lowerTitle.includes('散点') || lowerTitle.includes('分布')) {
    return 'scatter';
  }
  
  // 默认返回折线图
  return 'line';
};

// 类型定义
interface ChartSuggestion {
  suggest_reason?: string;
  completeOption?: any;
  chart_type?: string; // 图表类型
  echarts_type?: string; // 图表类型名称
  originalData?: any[]; // 原始数据
}

// 获取图表类型中文名称的函数
const getChartTypeName = (chart: ChartSuggestion): string => {
  // 直接使用echarts_type属性
  if (chart.echarts_type) {
    return chart.echarts_type;
  }
  
  return '';
};

// 判断是否为饼图
const isPieChart = (index: number): boolean => {
  // 如果有userData，检查当前选中的图表类型
  if (props.userData && props.userData.length > 0) {
    const availableTypes = getAvailableChartTypes();
    return availableTypes[selectedChartType.value] === '饼图';
  }
  // 如果有chartSuggestions，检查图表类型
  if (props.chartSuggestions && props.chartSuggestions[index]) {
    const chart = props.chartSuggestions[index];
    // 检查 chart_type 或 echarts_type
    if (chart.chart_type === 'pie' || chart.echarts_type === '饼图') {
      return true;
    }
    // 检查 completeOption 中的图表类型
    if (chart.completeOption?.series && Array.isArray(chart.completeOption.series)) {
      const series = chart.completeOption.series[0];
      if (series && series.type === 'pie') {
        return true;
      }
    }
  }
  return false;
};

// 获取图表的X轴名称
const getXAxisNameForChart = (index: number): string => {
  // 如果有userData，使用selectedXAxis
  if (props.userData && props.userData.length > 0 && selectedXAxis.value) {
    return selectedXAxis.value;
  }
  // 如果有chartSuggestions，尝试从completeOption中获取xAxis名称
  if (props.chartSuggestions && props.chartSuggestions[index]) {
    const chart = props.chartSuggestions[index];
    if (chart.completeOption?.xAxis?.name) {
      return chart.completeOption.xAxis.name;
    }
    // 如果completeOption是数组，取第一个
    if (Array.isArray(chart.completeOption?.xAxis) && chart.completeOption.xAxis[0]?.name) {
      return chart.completeOption.xAxis[0].name;
    }
  }
  return '';
};

// Props
const props = defineProps({
  chartSuggestions: {
    type: Array as () => ChartSuggestion[] | null,
    default: null
  },
  chartErrorMessage: {
    type: String as () => string | null | undefined,
    default: null
  },
  dataErrorMessage: {
    type: String as () => string | null | undefined,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  userData: {
    type: Array as () => any[] | null,
    default: null
  },
  columns: {
    type: Array as () => string[] | null,
    default: null
  },
  studioMode: {
    type: Boolean,
    default: false
  },
  maxHeight: {
    type: String,
    default: ''
  }
});

// 计算图表容器样式
const chartContainerClasses = computed(() => {
  const classes = ['bg-white rounded-lg flex flex-col'];

  if (props.studioMode) {
    // studio 模式下，不设置最大高度限制，完全由父容器控制
    classes.push('flex-1 min-h-0 h-full');
  } else {
    classes.push('flex-1 min-h-0');
  }

  return classes;
});

// 计算图表内容样式
const chartContentClasses = computed(() => {
  const classes = ['w-full bg-white rounded-md transition-opacity duration-300'];

  if (props.studioMode) {
    // Studio 模式：使用 flex-1 占满剩余空间，不设置最大高度限制
    classes.push('flex-1 min-h-[300px]');
  } else {
    // 非 Studio 模式：使用固定最小高度，确保图表容器始终有高度
    classes.push('min-h-[300px]');
  }

  return classes;
});


// 当前激活的标签页
const activeKey = ref('0');

// 图表控制相关状态
const selectedChartType = ref(0); // 当前选中的图表类型索引
const selectedXAxis = ref(''); // 当前选中的X轴
const selectedLeftYAxis = ref(''); // 当前选中的左Y轴
const selectedRightYAxis = ref(''); // 当前选中的右Y轴

// 初始化坐标轴选择
watch(() => props.columns, (newColumns) => {
  if (newColumns && newColumns.length > 0) {
    selectedXAxis.value = newColumns[0];
    
    // 找到数值列
    const numericColumns = newColumns.slice(1).filter(col => {
      // 检查是否为数值列
      if (props.userData && props.userData.length > 0) {
        const sampleValue = props.userData[0][col];
        return typeof sampleValue === 'number' || !isNaN(parseFloat(sampleValue));
      }
      return true;
    });
    
    // 设置左右Y轴
    if (numericColumns.length >= 2) {
      selectedLeftYAxis.value = numericColumns[0];
      selectedRightYAxis.value = numericColumns[1];
    } else if (numericColumns.length === 1) {
      selectedLeftYAxis.value = numericColumns[0];
      selectedRightYAxis.value = '__none__'; // 右Y轴默认未选择
    } else {
      selectedLeftYAxis.value = newColumns[1] || '__none__';
      selectedRightYAxis.value = '__none__'; // 右Y轴默认未选择
    }
  }
}, { immediate: true });

// 选择图表类型
const selectChartType = (index: number) => {
  // 获取可用的图表类型
  const availableTypes = getAvailableChartTypes();
  
  // 确保选择的索引在可用范围内
  if (index >= availableTypes.length) {
    // 如果选择的索引超出范围，重置为0
    selectedChartType.value = 0;
  } else {
    selectedChartType.value = index;
  }
  
  // 重新创建图表
  nextTick(() => {
    createChart(0);
  });
};

// 更新图表方法
const updateChart = () => {
  if (props.userData && props.userData.length > 0) {
    nextTick(() => {
      // 更新当前图表实例（索引为0）
      createChart(0);
    });
  }
};

// 监听坐标轴选择变化
watch([selectedXAxis, selectedLeftYAxis, selectedRightYAxis], () => {
  updateChart();
});

// 计算属性：处理Select显示值
const getLeftYAxisDisplayValue = computed(() => {
  if (!selectedLeftYAxis.value || selectedLeftYAxis.value === '__none__') {
    return '未选择';
  }
  return selectedLeftYAxis.value;
});

const getRightYAxisDisplayValue = computed(() => {
  if (!selectedRightYAxis.value || selectedRightYAxis.value === '__none__') {
    return '未选择';
  }
  return selectedRightYAxis.value;
});

// 计算属性：判断是否有多个图表方案
const hasMultipleCharts = computed(() => {
  return (props.chartSuggestions && props.chartSuggestions.length > 1) || 
         (props.userData && Array.isArray(props.userData) && props.userData.length > 0 && 
          props.columns && Array.isArray(props.columns) && props.columns.length > 0);
});

// 计算属性：判断是否有数据源
const hasDataSource = computed(() => {
  // 优先使用userData，如果有userData则使用userData
  const hasUserData = props.userData && Array.isArray(props.userData) && props.userData.length > 0 && 
                     props.columns && Array.isArray(props.columns) && props.columns.length > 0;
  
  // 如果没有userData，则使用chartSuggestions
  const hasChartSuggestions = props.chartSuggestions && props.chartSuggestions.length > 0;
  
  return hasUserData || hasChartSuggestions;
});

// 图表创建状态标志
const pendingChartCreation = ref(false);

// 图表状态管理
interface ChartState {
  instance: echarts.ECharts | null;      // 图表实例
  container: HTMLElement | null;         // 图表容器
  resizeObserver: ResizeObserver | null; // 尺寸观察器
}

// 图表状态集合
const chartStates = ref<Record<number, ChartState>>({});

// 初始化图表状态
function initChartState(index: number): void {
  if (!chartStates.value[index]) {
    chartStates.value[index] = {
      instance: null,
      container: null,
      resizeObserver: null
    };
  }
}

// 获取图表状态
function getChartState(index: number): ChartState {
  initChartState(index);
  return chartStates.value[index];
}

// 清理单个图表资源
function cleanupChartResources(index: number): void {
  const state = getChartState(index);
  
  // 清理图表实例
  if (state.instance) {
    try {
      state.instance.dispose();
      state.instance = null;
    } catch (e) {
      // 忽略清理错误
    }
  }
  
  // 清理观察器
  if (state.resizeObserver) {
    try {
      state.resizeObserver.disconnect();
      state.resizeObserver = null;
    } catch (e) {
      // 忽略错误
    }
  }
  
  // 清理初始观察器
  const initObserver = (state as any).initResizeObserver;
  if (initObserver) {
    try {
      initObserver.disconnect();
      (state as any).initResizeObserver = null;
    } catch (e) {
      // 忽略错误
    }
  }
}

// 清理所有图表资源
function cleanupAllChartResources(): void {
  Object.keys(chartStates.value).forEach(key => {
    cleanupChartResources(Number(key));
  });
}

// 设置图表容器的辅助函数
const setChartContainer = (el: Element | ComponentPublicInstance | null, index: number): void => {
  // 获取图表状态
  const state = getChartState(index);
  
  // 获取新的容器元素
  let newContainer: HTMLElement | null = null;
  if (el instanceof HTMLElement) {
    newContainer = el;
  } else if (el && 'el' in el && el.el instanceof HTMLElement) {
    // 处理Vue组件实例
    newContainer = el.el;
  } else {
    newContainer = null;
  }
  // 如果容器变化了
  if (state.container !== newContainer) {
    // 1. 如果有旧容器，移除旧的观察器
    if (state.container) {
      cleanupChartResources(index);
    }
    
    // 2. 如果有新容器，设置新的观察器
    if (newContainer) {
      // 使用 ResizeObserver 等待容器有实际尺寸后再创建图表
      // 这样可以避免强制设置内联样式，让 CSS 类正常工作
      const initResizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          
          // 只有当容器有有效尺寸时才创建图表
          if (width > CONFIG.MIN_VALID_WIDTH && height > 0) {
            // 取消观察，避免重复触发
            initResizeObserver.disconnect();
            
            // 设置正常的 ResizeObserver 用于后续尺寸变化
            setupResizeObserver(newContainer, index);
            
            // 检查是否有数据源，准备创建图表
            const activeIndex = Number(activeKey.value);
            if (index === activeIndex || hasDataSource.value) {
              nextTick(() => {
                const hasUserData = props.userData && Array.isArray(props.userData) && props.userData.length > 0 && 
                                   props.columns && Array.isArray(props.columns) && props.columns.length > 0;
                const hasChartSuggestionData = props.chartSuggestions?.[index]?.originalData && 
                                              Array.isArray(props.chartSuggestions[index].originalData) && 
                                              props.chartSuggestions[index].originalData.length > 0;
                
                if (hasUserData || hasChartSuggestionData) {
                  createChart(index);
                }
              });
            }
            
            break;
          }
        }
      });
      
      // 开始观察容器尺寸
      initResizeObserver.observe(newContainer);
      
      // 存储初始观察器，用于清理
      const state = getChartState(index);
      (state as any).initResizeObserver = initResizeObserver;
      
      // 注意：图表的创建已经由上面的 ResizeObserver 处理
      // 这里不需要额外处理，避免重复创建
    }
  }
  
  // 更新容器引用
  state.container = newContainer;
};

// 设置ResizeObserver
function setupResizeObserver(container: HTMLElement, index: number): void {
  const state = getChartState(index);
  
  // 清理之前的 ResizeObserver
  if (state.resizeObserver) {
    state.resizeObserver.disconnect();
    state.resizeObserver = null;
  }
  
  // 记录上一次的尺寸，用于避免不必要的 resize
  let lastWidth = container.clientWidth;
  let lastHeight = container.clientHeight;
  
  try {
    // 设置ResizeObserver
    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const width = entry.contentRect.width;
        const height = entry.contentRect.height;
        
        // 检查尺寸变化是否足够大，避免微小变化触发 resize
        const widthDiff = Math.abs(width - lastWidth);
        const heightDiff = Math.abs(height - lastHeight);
        const minChange = 5; // 最小变化阈值
                
        // 只有当尺寸变化足够大时才触发 resize
        if (widthDiff < minChange && heightDiff < minChange) {
          continue;
        }
        
        // 更新上一次的尺寸
        lastWidth = width;
        lastHeight = height;
        
        // 改进1: 即使宽度小于MIN_VALID_WIDTH，也记录日志，帮助调试
        if (width <= CONFIG.MIN_VALID_WIDTH) {
          // 改进2: 对于小宽度，尝试主动修复容器宽度
          if (container.style.width !== '100%') {
            // 使用渐进式动画优化重排
            container.style.willChange = 'transform, opacity';
            container.style.transition = 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
            container.style.opacity = '0.9';
            container.style.transform = 'scale(0.98)';
            container.style.width = '100%';
            
            // 使用 requestAnimationFrame 优化重排时机
            requestAnimationFrame(() => {
              const chart = state.instance;
              if (chart && !chart.isDisposed()) {
                chart.resize();
                
                // 恢复原始状态
                requestAnimationFrame(() => {
                  container.style.transform = 'scale(1)';
                  container.style.opacity = '1';
                  
                  // 清理优化属性
                  setTimeout(() => {
                    container.style.willChange = '';
                    container.style.transition = '';
                    container.style.transform = '';
                    container.style.opacity = '';
                  }, 250);
                });
              }
            });
          }
          continue;
        }
        
        // 容器宽度正常，调整图表大小
        const chart = state.instance;
        if (chart && !chart.isDisposed()) {
          // 使用渐进式动画优化，减少用户感知
          const container = chart.getDom();
          if (container) {
            // 添加平滑过渡动画
            container.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            container.style.opacity = '0.8';
            
            // 分阶段执行动画
            requestAnimationFrame(() => {
              container.style.transform = 'scale(0.98)';
              
              requestAnimationFrame(() => {
                container.style.transform = 'scale(1)';
                container.style.opacity = '1';
                
                // 执行 resize
                debouncedResizeChart(index, width);
                
                // 清理动画属性
                setTimeout(() => {
                  container.style.transition = '';
                  container.style.opacity = '';
                  container.style.transform = '';
                }, 300);
              });
            });
          } else {
            debouncedResizeChart(index, width);
          }
        }
      }
    });
    
    // 开始观察
    resizeObserver.observe(container);
    state.resizeObserver = resizeObserver;
  } catch (e) {
    // 忽略ResizeObserver设置错误
  }
}

// 防抖处理后的图表调整大小函数
const debouncedResizeChart = debounce((index: number, width: number) => {
  const state = getChartState(index);
  const chart = state.instance;
  
  if (chart && !chart.isDisposed()) {
    // 使用渐进式动画优化，减少用户感知
    const container = chart.getDom();
    if (container) {
      // 使用 will-change 提示浏览器优化
      container.style.willChange = 'transform, opacity';
      // 添加微妙的缩放动画
      container.style.transform = 'scale(0.99)';
      container.style.opacity = '0.95';
    }
    
    // 使用 requestAnimationFrame 确保在下一帧执行 resize
    requestAnimationFrame(() => {
      if (chart && !chart.isDisposed()) {
        // 不传入具体尺寸，让ECharts自动适应容器大小
        chart.resize();
        
        // 恢复原始状态
        requestAnimationFrame(() => {
          if (container) {
            container.style.transform = 'scale(1)';
            container.style.opacity = '1';
            
            // 清理优化属性
            setTimeout(() => {
              container.style.willChange = '';
              container.style.transform = '';
              container.style.opacity = '';
            }, 150);
          }
        });
      }
    });
  }
}, CONFIG.RESIZE_DEBOUNCE_DELAY);


// 创建图表实例
function createChart(index: number, retryCount = 0): void {
  try {
    // 获取图表状态
    const state = getChartState(index);
    const container = state.container;
    
    // 检查容器是否存在
    if (!container) {
      if (retryCount < CONFIG.MAX_RETRY_COUNT) {
        pendingChartCreation.value = true;
        window.setTimeout(() => createChart(index, retryCount + 1), CONFIG.CHECK_DELAY * (retryCount + 1));
      }
      return;
    }
    
    // 检查容器宽高是否正常
    // 由于使用了 ResizeObserver 等待容器尺寸就绪，这里应该已经有有效尺寸
    const containerWidth = container.clientWidth || container.offsetWidth;
    const containerHeight = container.clientHeight || container.offsetHeight;
    
    if (containerWidth <= CONFIG.MIN_VALID_WIDTH || containerHeight <= 0) {
      // 如果尺寸仍然异常，可能是 CSS 还未生效，等待一下
      if (retryCount < CONFIG.MAX_RETRY_COUNT) {
        pendingChartCreation.value = true;
        window.setTimeout(() => createChart(index, retryCount + 1), CONFIG.CHECK_DELAY * (retryCount + 1));
        return;
      } else {
        // CSS 类已经设置了 min-h-[300px]，如果还是 0，可能是布局问题
        // 这种情况下不创建图表，避免渲染错误
        pendingChartCreation.value = false;
        return;
      }
    }
    
    // 获取图表数据
    let chartData: any[] = [];
    let columns: string[] = [];
    
    // 优先使用userData和columns（来自dataset）
    if (props.userData && Array.isArray(props.userData) && props.userData.length > 0 && 
        props.columns && Array.isArray(props.columns) && props.columns.length > 0) {
      chartData = props.userData;
      columns = props.columns;
    } else {
      // 备用方案：从chartSuggestions获取数据
      const chartSuggestion = props.chartSuggestions?.[index];
      if (chartSuggestion?.originalData && Array.isArray(chartSuggestion.originalData) && chartSuggestion.originalData.length > 0) {
        chartData = chartSuggestion.originalData;
        if (chartData.length > 0) {
          columns = Object.keys(chartData[0]);
        }
      } else {
        pendingChartCreation.value = false;
        return;
      }
    }
    
    if (chartData.length === 0) {
      pendingChartCreation.value = false;
      return;
    }
    
    // 根据选中的图表类型确定配置
    const availableTypes = getAvailableChartTypes();
    const availableChartTypes = CHART_TYPES.TYPES.filter((_, index) => 
      availableTypes.includes(CHART_TYPES.TITLES[index])
    );
    
    const chartType = availableChartTypes[selectedChartType.value];
    const displayType = CHART_TYPE_TO_DISPLAY_TYPE[chartType];
    
    if (!displayType) {
      pendingChartCreation.value = false;
      return;
    }
    
    // 使用仪表盘的图表配置函数
    // 准备数据：chartData 已经是数组对象格式，可以直接使用
    const tableData = chartData;
    
    // 获取字段映射
    const xField = selectedXAxis.value || columns[0] || '';
    const leftYField = selectedLeftYAxis.value && selectedLeftYAxis.value !== '__none__' 
      ? selectedLeftYAxis.value 
      : undefined;
    const rightYField = selectedRightYAxis.value && selectedRightYAxis.value !== '__none__' 
      ? selectedRightYAxis.value 
      : undefined;
    
    // 对于饼图，使用 yField（第一个数值字段）
    const yField = leftYField || (columns.find(col => {
      const firstValue = tableData[0]?.[col];
      return typeof firstValue === 'number' || (!isNaN(parseFloat(firstValue)) && firstValue !== '');
    }) || columns[1] || '');
    
    // 调用仪表盘的图表配置函数
    const isMobile = window.innerWidth < 768;
    let chartOption = getChartOption({
      tableData,
      columns,
      displayType,
      xField,
      yField,
      leftYField,
      rightYField,
      isMobile,
      columnNameMapping: undefined
    });
    
    if (!chartOption) {
      pendingChartCreation.value = false;
      return;
    }
    
    // 清理可能存在的旧实例
    cleanupChartResources(index);
    
    // 重新初始化图表容器
    container.innerHTML = '';
    
    // 容器尺寸已经通过 ResizeObserver 确认有效，直接创建图表
    // 不需要强制设置内联样式，让 CSS 类正常工作
    
    // 创建图表实例 - ECharts 会自动适应容器大小
    const chart = echarts.init(container, null, {
      renderer: 'canvas'
    });
    
    // 添加hover事件处理
    chart.on('mouseover', (params: any) => {
      if (params.componentType === 'series' && typeof params.seriesIndex === 'number' && typeof params.dataIndex === 'number') {
        // 获取当前图表类型
        const currentOption = chart.getOption();
        const series = currentOption.series as any[];
        if (series && series[params.seriesIndex]) {
          const currentSeries = series[params.seriesIndex];
          
          // 只对非饼图类型执行 setOption，避免饼图图例和 tooltip 消失
          if (currentSeries.type !== 'pie') {
            const currentData = currentSeries.data as any[];
            
            if (currentData && currentData[params.dataIndex]) {
              // 保持原始数据值，显示标签
              const originalValue = currentData[params.dataIndex];
              currentData[params.dataIndex] = {
                value: originalValue.value || originalValue,
                label: {
                  show: true,
                  position: 'top',
                  fontSize: 10,
                  color: '#333'
                }
              };
              chart.setOption({ series: series });
            }
          }
        }
      }
    });
    
    // 鼠标离开时隐藏标签
    chart.on('mouseout', (params: any) => {
      if (params.componentType === 'series' && typeof params.seriesIndex === 'number' && typeof params.dataIndex === 'number') {
        // 获取当前图表类型
        const currentOption = chart.getOption();
        const series = currentOption.series as any[];
        if (series && series[params.seriesIndex]) {
          const currentSeries = series[params.seriesIndex];
          
          // 只对非饼图类型执行 setOption，避免饼图图例和 tooltip 消失
          if (currentSeries.type !== 'pie') {
            const currentData = currentSeries.data as any[];
            
            if (currentData && currentData[params.dataIndex]) {
              // 保持原始数据值，隐藏标签
              const originalValue = currentData[params.dataIndex];
              currentData[params.dataIndex] = {
                value: originalValue.value || originalValue,
                label: {
                  show: false,
                  position: 'top',
                  fontSize: 10,
                  color: '#333'
                }
              };
              chart.setOption({ series: series });
            }
          }
        }
      }
    });
    
    // 设置图表配置
    chart.setOption(chartOption);
    state.instance = chart;
    
    // 获取 ECharts 实例的实际容器元素
    const echartsContainer = chart.getDom();
    if (echartsContainer) {
      // 重新设置 ResizeObserver 监听 ECharts 的实际容器
      setupResizeObserver(echartsContainer, index);
    }
    
    // 图表成功创建，重置标志
    pendingChartCreation.value = false;
    
    // 图表渲染完成后触发滚动到底部
    triggerScrollToBottom();
  } catch (e: any) {
    // 出现错误时也重置标志，避免无限尝试
    pendingChartCreation.value = false;
  }

}



// 处理标签页切换
function handleTabChange(activeKey: string): void {
  const activeIndex = Number(activeKey);
  if (isNaN(activeIndex) || activeIndex < 0) return;
  
  // 确保在DOM更新后再渲染图表
  nextTick(() => {
    // 获取图表状态
    const state = getChartState(activeIndex);
    const container = state.container;
    
    // 检查容器是否存在
    if (!container) {
      // 标记为待创建，当容器可用时会在setChartContainer中处理
      pendingChartCreation.value = true;
      return;
    }
    
    // 确保容器样式正确
    container.style.width = '100%';
    container.style.height = `${CONFIG.DEFAULT_HEIGHT}px`;
    
    // 检查是否有数据源
    const hasUserData = props.userData && Array.isArray(props.userData) && props.userData.length > 0 && 
                       props.columns && Array.isArray(props.columns) && props.columns.length > 0;
    const hasChartSuggestionData = props.chartSuggestions?.[activeIndex]?.originalData && 
                                  Array.isArray(props.chartSuggestions[activeIndex].originalData) && 
                                  props.chartSuggestions[activeIndex].originalData.length > 0;
    
    // 如果有userData，则所有索引都是有效的（因为会循环创建4种图表）
    if (hasUserData) {
      // 对于userData，所有索引都是有效的，因为会循环创建4种图表类型
    } else if (!hasChartSuggestionData) {
      return;
    }
    
    // 检查是否已有实例
    if (state.instance && !state.instance.isDisposed()) {
      // 调整已有实例的大小
      state.instance.resize();
      
      // 增加: 延迟验证容器尺寸是否正确
      setTimeout(() => {
        validateAndFixChartSize(activeIndex);
      }, CONFIG.CHECK_DELAY);
    } else {
      // 创建新实例
      createChart(activeIndex);
      // 重置标志
      pendingChartCreation.value = false;
      
      // 增加: 延迟验证容器尺寸是否正确
      setTimeout(() => {
        validateAndFixChartSize(activeIndex);
      }, CONFIG.CHECK_DELAY * 2); // 给新创建的图表多一点时间
    }
  });
}

// 新增函数: 验证并修复图表尺寸
function validateAndFixChartSize(index: number): void {
  const state = getChartState(index);
  const container = state.container;
  const chart = state.instance;
  
  if (!container || !chart || chart.isDisposed()) return;
  
  // 获取容器当前宽度
  const containerWidth = container.clientWidth;
  
  // 如果宽度异常，尝试修复
  if (containerWidth <= CONFIG.MIN_VALID_WIDTH) {
    // 强制设置容器宽度为100%
    container.style.width = '100%';
    
    // 给DOM时间更新后再调整图表大小
    setTimeout(() => {
      if (chart && !chart.isDisposed()) {
        chart.resize();
      }
    }, CONFIG.CHECK_DELAY);
  }
}

// 处理窗口大小变化
function handleResize(): void {
  const activeIndex = Number(activeKey.value);
  const state = getChartState(activeIndex);
  
  if (state.instance && !state.instance.isDisposed()) {
    state.instance.resize();
  }
}

// 监听数据变化
watch([() => props.chartSuggestions, () => props.userData, () => props.columns], () => {
  if (!hasDataSource.value) return;
  
  // 重置activeKey
  activeKey.value = '0';
  
  // 检查当前选择的图表类型是否仍然可用
  const availableTypes = getAvailableChartTypes();
  if (selectedChartType.value >= availableTypes.length) {
    // 如果当前选择不可用，重置为0
    selectedChartType.value = 0;
  }
  
  // 数据变化时清理所有图表
  cleanupAllChartResources();
  
  // 标记需要创建图表
  pendingChartCreation.value = true;
  
  // 不再直接调用createChart，而是等待DOM更新后再创建
}, { deep: true });

// 组件挂载
onMounted(() => {
  window.addEventListener('resize', handleResize);

  // 初始渲染
  nextTick(() => {
    if (hasDataSource.value) {
      // 直接调用handleTabChange而不是renderActiveChart
      handleTabChange(activeKey.value);

      // 添加额外的图表尺寸检查，确保图表在各种情况下都能正确显示
      setTimeout(() => {
        const activeIndex = Number(activeKey.value);
        validateAndFixChartSize(activeIndex);

        // 打印当前容器尺寸信息，帮助调试
        const state = getChartState(activeIndex);
      }, CONFIG.CHECK_DELAY * 3);
    }
  });
});

// {{CHENGQI:
// Action: Added
// Reason: 修复智能体切换时图表宽度异常问题，使用onActivated监听组件激活
// Principle_Applied: KISS - 使用Vue原生生命周期钩子，实现简单直接
// Optimization: 专门针对智能体切换场景，不影响正常渲染流程
// Architectural_Note (AR): 利用Vue的keep-alive机制，在组件激活时检查图表状态
// Documentation_Note (DW): 相关文档已更新至chart_width_fix_workspace/智能体切换图表宽度异常修复.md
// }}
// {{START MODIFICATIONS}}
// + 组件激活时的图表状态检查和修复
onActivated(() => {
  // 确保DOM完全准备好
  nextTick(() => {
    setTimeout(() => {
      const activeIndex = Number(activeKey.value);
      const state = getChartState(activeIndex);

      // 检查是否有图表数据和容器
      if (state.container && hasDataSource.value) {
        const containerWidth = state.container.clientWidth;

        // 检测宽度异常并修复
        if (containerWidth <= CONFIG.MIN_VALID_WIDTH) {
          // 强制设置容器宽度
          state.container.style.width = '100%';
          // 重新创建图表
          createChart(activeIndex);
        } else if (state.instance && !state.instance.isDisposed()) {
          // 容器宽度正常，但确保图表尺寸正确
          state.instance.resize();
        } else if (!state.instance) {
          // 检查是否有数据源
          const hasUserData = props.userData && Array.isArray(props.userData) && props.userData.length > 0 && 
                             props.columns && Array.isArray(props.columns) && props.columns.length > 0;
          const hasChartSuggestionData = props.chartSuggestions?.[activeIndex]?.originalData && 
                                        Array.isArray(props.chartSuggestions[activeIndex].originalData) && 
                                        props.chartSuggestions[activeIndex].originalData.length > 0;
          
          // 如果有userData，则所有索引都是有效的（因为会循环创建4种图表）
          if (hasUserData || hasChartSuggestionData) {
          // 没有图表实例但有数据，创建图表
          createChart(activeIndex);
          }
        }
      }
    }, 200); // 给DOM稳定的时间，确保容器完全准备好
  });
});
// {{END MODIFICATIONS}}

// 添加组件更新钩子，处理DOM更新后的情况
onUpdated(() => {
  if (hasDataSource.value) {
    const activeIndex = Number(activeKey.value);
    // 延迟验证，确保DOM已更新
    setTimeout(() => {
      validateAndFixChartSize(activeIndex);
    }, CONFIG.CHECK_DELAY);
  }
});

// 组件卸载
onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  cleanupAllChartResources();
});

// 导出方法
defineExpose({
  renderChart: createChart
});
</script>

 
 
