<template>
  <div class="w-full font-inherit bg-transparent">
    <StageHeader
      :show="showCollapseHeader"
      :status="currentStatus"
      :status-text="currentStatusText"
      :total-elapsed-time="totalElapsedTime"
      :collapsed="isCollapsed"
      :show-timeout-hint="showTimeoutHint"
      @toggle="toggleCollapse"
    />

    <transition-group
      v-if="!isCollapsed"
      name="fade"
      tag="ol"
      class="m-0 p-0 block"
      role="list"
    >
      <li
        v-for="(stage, index) in displayStages"
        :key="stage.stageId || `${stage.key}-${index}`"
        class="list-none py-1.5"
      >
        <div class="grid grid-cols-[1fr_auto] gap-3 items-center max-md:grid-cols-1 max-md:gap-4">
          <div class="min-w-0 flex items-center gap-2.5">
            <!-- 有详情的节点：显示可点击的按钮 -->
            <button
              v-if="hasStageDetails(stage)"
              type="button"
              class="inline-flex items-center gap-1.5 border-0 bg-transparent p-0 cursor-pointer font-inherit text-gray-800 min-w-0 hover:[&_.arrow-icon]:text-gray-900"
              @click="toggleStage(getStageToggleKey(stage, index))"
              :aria-expanded="stageExpandStates[getStageToggleKey(stage, index)] ? 'true' : 'false'"
              :aria-controls="`detail-${getStageToggleKey(stage, index)}`"
            >
              <!-- 节点状态图标 -->
              <StatusIcon
                :status="stage.status"
                :expanded="!!stageExpandStates[getStageToggleKey(stage, index)]"
                :status-text-map="STATUS_TEXT_MAP"
              />
              <!-- 展开/收起箭头图标 -->
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                class="w-3.5 h-3.5 text-gray-500 transition-transform duration-200 arrow-icon"
                :class="{ 'rotate-90': stageExpandStates[getStageToggleKey(stage, index)] }"
                aria-hidden="true"
              >
                <path d="m9 18 6-6-6-6" />
              </svg>
              <!-- 阶段序号 -->
              <span class="text-[11px] text-gray-500 flex-shrink-0 max-md:text-[10px]">#{{ getStageDisplayNumber(index) }}</span>
              <!-- 阶段标题 -->
              <span class="text-sm font-medium text-gray-900 max-w-[14rem] overflow-hidden text-ellipsis whitespace-nowrap max-md:text-[13px] max-md:max-w-[12rem]" :title="getStageTitle(stage)">
                {{ getStageTitle(stage) }}
              </span>
            </button>

            <!-- 没有详情的节点：显示静态内容 -->
            <div
              v-else
              class="inline-flex items-center gap-1.5 text-gray-800 min-w-0"
            >
              <!-- 节点状态图标 -->
              <StatusIcon :status="stage.status" :status-text-map="STATUS_TEXT_MAP" />
              <!-- 阶段序号 -->
              <span class="text-[11px] text-gray-500 flex-shrink-0 max-md:text-[10px]">#{{ getStageDisplayNumber(index) }}</span>
              <!-- 阶段标题 -->
              <span class="text-sm font-medium text-gray-900 max-w-[14rem] overflow-hidden text-ellipsis whitespace-nowrap max-md:text-[13px] max-md:max-w-[12rem]" :title="getStageTitle(stage)">
                {{ getStageTitle(stage) }}
              </span>
            </div>

            <!-- 阶段摘要信息 -->
            <span
              v-if="getFormattedSummary(stage)"
              class="text-xs text-gray-500 max-w-[24rem] whitespace-nowrap overflow-hidden text-ellipsis max-md:text-[11px] max-md:max-w-full"
              :class="{ 'text-orange-500 font-medium': stage.status === 'failed' }"
            >
              · {{ getFormattedSummary(stage) }}
            </span>

            <!-- 阶段耗时 -->
            <span v-if="getStageElapsedTime(stage)" class="text-xs text-green-600 font-medium flex-shrink-0">
              · {{ formatElapsedTime(getStageElapsedTime(stage)!) }}
            </span>
          </div>
        </div>

        <transition name="collapse">
          <div
            v-if="hasStageDetails(stage) && stageExpandStates[getStageToggleKey(stage, index)]"
            :id="`detail-${getStageToggleKey(stage, index)}`"
            class="mt-1.5 grid grid-cols-[1fr_auto] gap-3"
          >
            <div class="col-span-1 p-3 border border-gray-200 rounded-lg bg-white shadow-sm max-w-full overflow-hidden break-words max-md:p-2.5">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-semibold text-gray-700">详情</span>
                <span v-if="(stage as SqlStageStateItem & { cacheHit?: boolean }).cacheHit" class="text-[11px] text-blue-600 bg-blue-50 rounded-full px-2 py-0.5 border border-blue-200">⚡ 缓存命中</span>
              </div>

              <div class="flex flex-col gap-3 max-w-full overflow-hidden space-y-4">
                <!-- 多路召回详情 -->
                <div
                  v-if="stage.key === 'knowledge_retrieval' && getKnowledgeDetails(stage, index).length"
                  class="w-full min-w-0"
                >
                  <MarkdownMessage
                    v-if="stage.description && !stage.metadata?.enriched?.filteringSteps"
                    :content="stage.description"
                    :messageId="`stage-${messageId}-${getStageToggleKey(stage, index)}`"
                    class="detail-markdown mt-3"
                  />

                  <!-- 过滤步骤详情 -->
                  <div
                    v-if="stage.metadata?.enriched?.filteringSteps && stage.metadata.enriched.filteringSteps.length"
                    class="mt-4 space-y-3"
                  >
                    <div
                      v-for="(step, stepIdx) in stage.metadata.enriched.filteringSteps"
                      :key="step.stepKey"
                      class="bg-white border border-gray-200 rounded-[10px] overflow-hidden transition-all mb-3 hover:border-gray-300 hover:shadow-sm"
                    >
                      <div class="flex items-center justify-between gap-3 px-4 py-3.5 bg-gradient-to-r from-gray-50 to-white cursor-pointer transition-all border-b border-gray-100 hover:from-gray-100 hover:to-gray-50" @click="toggleFilteringStep(`${getStageToggleKey(stage, index)}-step-${stepIdx}`)">
                        <div class="flex items-center gap-3 flex-1">
                          <span class="inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex-shrink-0">{{ Number(stepIdx) + 1 }}</span>
                          <h4 class="text-sm font-semibold text-gray-900 m-0 flex-1">{{ step.stepName }}</h4>
                          <span class="text-xs font-semibold text-green-600 bg-green-50 px-2.5 py-1 rounded-md border border-green-200 flex-shrink-0">{{ step.count }} 条</span>
                        </div>
                        <button type="button" class="text-xs text-blue-600 bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-md cursor-pointer transition-all flex-shrink-0 font-medium hover:bg-blue-100 hover:border-blue-300 hover:text-blue-700">
                        {{ isFilteringStepExpanded(`${getStageToggleKey(stage, index)}-step-${stepIdx}`) ? '收起' : '展开' }}
                        </button>
                      </div>

                      <div
                        v-if="isFilteringStepExpanded(`${getStageToggleKey(stage, index)}-step-${stepIdx}`)"
                        class="p-4 bg-gray-50 border-t border-gray-200"
                      >
                        <p v-if="step.description" class="text-[13px] text-gray-700 m-0 mb-3 px-3 py-2.5 bg-white border-l-[3px] border-blue-500 rounded-md">{{ step.description }}</p>

                        <div v-if="step.knowledgeList && step.knowledgeList.length" class="space-y-2 mt-3">
                          <div
                            v-for="(item, idx) in step.knowledgeList"
                            :key="`${step.stepKey}-${idx}`"
                            class="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden transition-all w-full max-w-full min-w-0 box-border hover:border-gray-300 hover:shadow-sm"
                          >
                            <div class="flex items-center gap-2 p-3 bg-white cursor-pointer transition-all overflow-hidden w-full max-w-full min-w-0 box-border hover:bg-gray-50">
                              <div class="flex items-start gap-2 flex-1 min-w-0">
                                <span class="text-[11px] font-semibold text-gray-500 bg-gray-200 px-1.5 py-0.5 rounded flex-shrink-0">#{{ item.index ?? (Number(idx) + 1) }}</span>
                                <span class="text-[11px] font-semibold px-2 py-0.5 rounded uppercase flex-shrink-0" :class="getKnowledgeTypeClass(item.type || 'unknown')">{{ item.type || 'unknown' }}</span>
                                <h5
                                  class="flex-1 min-w-0 m-0 break-words text-[13px] font-medium text-gray-900"
                                  :title="getKnowledgeTitle(item)"
                                >
                                  {{ getKnowledgeTitle(item) }}
                                </h5>
                              </div>
                              <div class="flex items-center gap-2 flex-shrink-0 ml-2">
                                <button
                                  type="button"
                                  @click.stop="toggleKnowledgeItem(getKnowledgeItemKey(step.stepKey, idx))"
                                  class="text-xs text-blue-600 bg-transparent border-0 px-2 py-1 rounded cursor-pointer transition-all flex-shrink-0 hover:bg-blue-50 hover:text-blue-700"
                                >
                                  {{ isKnowledgeItemExpanded(getKnowledgeItemKey(step.stepKey, idx)) ? '收起' : '展开' }}
                                </button>
                                <span v-if="item.score" class="text-[11px] font-mono text-green-600 bg-green-50 px-1.5 py-0.5 rounded flex-shrink-0">{{ Number(item.score).toFixed(4) }}</span>
                              </div>
                            </div>

                            <!-- 知识库项目内容 -->
                            <KnowledgeItemContent
                              v-if="isKnowledgeItemExpanded(getKnowledgeItemKey(step.stepKey, idx))"
                              :item="item"
                              :get-knowledge-base-link="getKnowledgeBaseLink"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 原有的知识列表（当没有 filteringSteps 时显示） -->
                  <KnowledgeList
                    v-else-if="getKnowledgeDetails(stage, index).length"
                    :items="getKnowledgeDetails(stage, index)"
                    :expanded-items="expandedKnowledgeItems"
                    :get-knowledge-base-link="getKnowledgeBaseLink"
                    :get-knowledge-title="getKnowledgeTitle"
                    :get-knowledge-type-class="getKnowledgeTypeClass"
                    :get-item-key="(idx) => getKnowledgeItemKey(getStageToggleKey(stage, index), idx)"
                    class="mt-3"
                    @toggle-item="(idx) => toggleKnowledgeItem(getKnowledgeItemKey(getStageToggleKey(stage, index), idx))"
                  />
                </div>

                <!-- 通用说明（知识召回阶段已有详细列表，不再重复展示描述） -->
                <div
                  v-if="shouldShowStageDescription(stage, index)"
                >
                  <MarkdownMessage
                    :content="stage.description!"
                    :messageId="`stage-${messageId}-${getStageToggleKey(stage, index)}`"
                    class="detail-markdown"
                  />
                </div>
                <p
                  v-else-if="shouldShowEmptyDescription(stage, index)"
                  class="text-xs leading-relaxed text-gray-400 mb-1.5 italic"
                >
                  暂无更多说明
                </p>

                <p v-if="stage.errorMessage" class="text-xs leading-relaxed text-red-700 bg-red-50 rounded-md p-1.5 border border-red-200 break-words whitespace-pre-wrap">
                  错误：{{ stage.errorMessage }}
                </p>

                <p v-if="stage.suggestion" class="text-xs leading-relaxed text-blue-700 mb-1.5">
                  建议：{{ stage.suggestion }}
                </p>

                <!-- Enriched metadata sections -->
                <div
                  v-if="stage.metadata?.enriched"
                  class="mt-1 space-y-4"
                >
                  <div
                    v-if="stage.metadata.enriched.requestParams"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">请求参数</span>
                      <button
                        type="button"
                        class="text-xs text-blue-600 bg-transparent border-0 cursor-pointer p-0 hover:underline"
                        @click="toggleDetailSection(`${getStageToggleKey(stage, index)}-request-params`)"
                      >
                        {{ isSectionExpanded(`${getStageToggleKey(stage, index)}-request-params`) ? '收起' : '展开' }}
                      </button>
                    </div>
                    <pre
                      v-if="isSectionExpanded(`${getStageToggleKey(stage, index)}-request-params`)"
                      class="bg-slate-900 text-slate-100 rounded-lg text-xs font-mono p-2.5 whitespace-pre-wrap break-words overflow-wrap-break-word overflow-x-auto"
                    >{{ formatJson(stage.metadata.enriched.requestParams) }}</pre>
                    <div v-else class="text-xs text-gray-700 bg-gray-50 rounded-lg p-2 border border-dashed border-gray-200 break-words">
                      {{ getJsonPreview(stage.metadata.enriched.requestParams, TIMELINE_CONFIG.JSON_PREVIEW_LENGTH) }}
                    </div>
                  </div>

                  <div
                    v-if="stage.metadata.enriched.llmDetails && stage.key !== 'sql_validation'"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">LLM 配置</span>
                    </div>
                    <div class="grid gap-1.5 text-xs text-gray-700">
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">模型</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.llmDetails.model_name }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.llmDetails.model_version" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">版本</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.llmDetails.model_version }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.llmDetails.request_params" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">温度</span>
                        <span class="font-semibold text-gray-900">
                          {{ stage.metadata.enriched.llmDetails.request_params.temperature ?? '默认' }}
                        </span>
                      </div>
                      <div v-if="stage.metadata.enriched.llmDetails.token_usage" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">Token</span>
                        <span class="font-semibold text-gray-900">
                          提示 {{ stage.metadata.enriched.llmDetails.token_usage.prompt_tokens ?? '-' }} / 输出 {{ stage.metadata.enriched.llmDetails.token_usage.completion_tokens ?? '-' }}
                        </span>
                      </div>
                      <div v-if="stage.metadata.enriched.llmDetails.response_time_ms" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">耗时</span>
                        <span class="font-semibold text-gray-900">{{ (stage.metadata.enriched.llmDetails.response_time_ms / 1000).toFixed(2) }}s</span>
                      </div>
                    </div>
                  </div>

                  <!-- LLM 请求体（仅用于 sql_generation 阶段，其他阶段有专门的展示区域） -->
                  <LlmRequestSection
                    v-if="stage.key === 'sql_generation' && stage.metadata.enriched.llmRequest"
                    title="LLM 请求体"
                    :data="stage.metadata.enriched.llmRequest"
                    :preview="`包含 ${stage.metadata.enriched.llmRequest.messages?.length ?? 0} 条消息 · 模型 ${stage.metadata.enriched.llmRequest.model || stage.metadata.enriched.llmRequest.app_code || '未指定'}`"
                    copy-title="复制请求体"
                    :expanded="isSectionExpanded(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @toggle="toggleDetailSection(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @copy="(data) => copyJson(data)"
                  />

                  <div
                    v-if="stage.metadata.enriched.llmStage"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">LLM 响应摘要</span>
                    </div>
                    <div class="text-xs text-gray-700 space-y-2">
                      <div v-if="stage.metadata.enriched.llmStage.requestExcerpt">
                        <div class="text-xs font-semibold text-gray-700 mb-1">请求片段</div>
                        <div class="text-xs text-gray-900 leading-relaxed bg-gray-50 p-2 rounded-lg whitespace-pre-wrap break-words">{{ stage.metadata.enriched.llmStage.requestExcerpt }}</div>
                      </div>
                      <div v-if="stage.metadata.enriched.llmStage.responseExcerpt">
                        <div class="text-xs font-semibold text-gray-700 mb-1">响应片段</div>
                        <div class="text-xs text-gray-900 leading-relaxed bg-gray-50 p-2 rounded-lg whitespace-pre-wrap break-words">{{ stage.metadata.enriched.llmStage.responseExcerpt }}</div>
                      </div>
                      <div v-if="stage.metadata.enriched.llmStage.truncated" class="text-[11px] text-orange-500">
                        内容已截断，完整内容可通过 Trace 查看
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="stage.metadata.enriched.validation"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">SQL 校验结果</span>
                    </div>
                    <div class="grid gap-1.5 text-xs text-gray-700">
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">通过校验</span>
                        <span class="font-semibold text-gray-900">
                          {{ formatValue(stage.metadata.enriched.validation.valid) }}
                        </span>
                      </div>
                      <div v-if="stage.metadata.enriched.validation.confidence !== undefined" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">置信度</span>
                        <span class="font-semibold text-gray-900">
                          {{ (stage.metadata.enriched.validation.confidence * 100).toFixed(1) }}%
                        </span>
                      </div>
                      <div v-if="stage.metadata.enriched.validation.recommendation" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">建议</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.validation.recommendation }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 问题理解阶段的 LLM 请求信息 -->
                  <LlmRequestSection
                    v-if="stage.key === 'question_understanding' && stage.metadata.enriched.llmRequest"
                    title="LLM 请求参数"
                    :data="stage.metadata.enriched.llmRequest"
                    :preview="`原始问题：${stage.metadata.enriched.llmRequest.original_question || '未提供'} · 模型：${stage.metadata.enriched.llmRequest.app_code || '未指定'}`"
                    copy-title="复制请求参数"
                    :expanded="isSectionExpanded(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @toggle="toggleDetailSection(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @copy="(data) => copyJson(data)"
                  />

                  <!-- 问题理解阶段的 LLM 响应信息 -->
                  <LlmRequestSection
                    v-if="stage.key === 'question_understanding' && stage.metadata.enriched.llmResponse"
                    title="LLM 响应结果"
                    :data="stage.metadata.enriched.llmResponse"
                    :preview="`改写成功：${stage.metadata.enriched.llmResponse.rewrite_success ? '是' : '否'} · 是否改写：${stage.metadata.enriched.llmResponse.is_rewritten ? '是' : '否'}`"
                    copy-title="复制响应结果"
                    :expanded="isSectionExpanded(`${getStageToggleKey(stage, index)}-llm-response`)"
                    @toggle="toggleDetailSection(`${getStageToggleKey(stage, index)}-llm-response`)"
                    @copy="(data) => copyJson(data)"
                  />

                  <!-- SQL 校验阶段的 LLM 请求信息 -->
                  <LlmRequestSection
                    v-if="stage.key === 'sql_validation' && stage.metadata.enriched.llmRequest"
                    title="LLM 请求体"
                    :data="stage.metadata.enriched.llmRequest"
                    :preview="`包含 ${stage.metadata.enriched.llmRequest.messages?.length ?? 0} 条消息 · 模型 ${stage.metadata.enriched.llmRequest.model || stage.metadata.enriched.llmRequest.app_code || '未指定'}`"
                    copy-title="复制请求体"
                    :expanded="isSectionExpanded(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @toggle="toggleDetailSection(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @copy="(data) => copyJson(data)"
                  />

                  <div
                    v-if="stage.metadata.enriched.correction"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">SQL 自修复</span>
                    </div>
                    <div class="grid gap-1.5 text-xs text-gray-700 mb-2">
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">修复结果</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.correction.success ? '成功' : '失败' }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.correction.reason" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">原因</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.correction.reason }}</span>
                      </div>
                    </div>
                    <div v-if="stage.metadata.enriched.correction.originalSql" class="mt-2">
                      <div class="text-xs font-semibold text-gray-700 mb-1">原始 SQL</div>
                      <pre class="bg-gray-900 whitespace-pre w-full box-border overflow-x-auto rounded-lg text-xs font-mono p-2.5 text-gray-200">{{ formatSql(stage.metadata.enriched.correction.originalSql) }}</pre>
                    </div>
                    <div v-if="stage.metadata.enriched.correction.newSql" class="mt-2">
                      <div class="text-xs font-semibold text-gray-700 mb-1">修复后 SQL</div>
                      <pre class="bg-gray-900 whitespace-pre w-full box-border overflow-x-auto rounded-lg text-xs font-mono p-2.5 text-gray-200">{{ formatSql(stage.metadata.enriched.correction.newSql) }}</pre>
                    </div>
                  </div>

                  <!-- SQL 纠正阶段的 LLM 请求信息 -->
                  <LlmRequestSection
                    v-if="stage.key === 'sql_correction' && stage.metadata.enriched.llmRequest"
                    title="LLM 请求体"
                    :data="stage.metadata.enriched.llmRequest"
                    :preview="`包含 ${stage.metadata.enriched.llmRequest.messages?.length ?? 0} 条消息 · 模型 ${stage.metadata.enriched.llmRequest.model || stage.metadata.enriched.llmRequest.app_code || '未指定'}`"
                    copy-title="复制请求体"
                    :expanded="isSectionExpanded(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @toggle="toggleDetailSection(`${getStageToggleKey(stage, index)}-llm-request`)"
                    @copy="(data) => copyJson(data)"
                  />

                  <div
                    v-if="stage.metadata.enriched.rerankDetails"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">重排序详情</span>
                    </div>
                    <div class="grid gap-1.5 text-xs text-gray-700">
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">模型</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.rerankDetails.model_used || '-' }}</span>
                      </div>
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">排序前</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.rerankDetails.before_count ?? '-' }}</span>
                      </div>
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">排序后</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.rerankDetails.after_order?.length ?? '-' }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.rerankDetails.processing_time_ms" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">耗时</span>
                        <span class="font-semibold text-gray-900">
                          {{ (stage.metadata.enriched.rerankDetails.processing_time_ms / 1000).toFixed(2) }}s
                        </span>
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="stage.metadata.enriched.execution"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">数据执行</span>
                    </div>
                    <div class="grid gap-1.5 text-xs text-gray-700">
                      <div class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">是否成功</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.execution.success ? '成功' : '失败' }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.execution.rows !== undefined" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">返回行数</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.execution.rows }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.execution.limitApplied !== undefined" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">LIMIT</span>
                        <span class="font-semibold text-gray-900">
                          {{ stage.metadata.enriched.execution.limitApplied ? `已应用 (${stage.metadata.enriched.execution.limitValue ?? '-'})` : '未应用' }}
                        </span>
                      </div>
                      <div v-if="stage.metadata.enriched.execution.errorMessage" class="text-xs text-red-700 bg-red-50 border border-red-200 break-words whitespace-pre-wrap leading-relaxed p-2 rounded-lg">
                        {{ stage.metadata.enriched.execution.errorMessage }}
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="stage.metadata.enriched.executionSummary"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">执行摘要</span>
                    </div>
                    <div class="grid gap-1.5 text-xs text-gray-700">
                      <div v-if="stage.metadata.enriched.executionSummary.row_count !== undefined" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">行数</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.executionSummary.row_count }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.executionSummary.limit_applied !== undefined" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">LIMIT</span>
                        <span class="font-semibold text-gray-900">
                          {{ stage.metadata.enriched.executionSummary.limit_applied ? `已应用 (${stage.metadata.enriched.executionSummary.limit_value ?? '-'})` : '未应用' }}
                        </span>
                      </div>
                      <div v-if="stage.metadata.enriched.executionSummary.db_type" class="flex items-center justify-between gap-3">
                        <span class="text-gray-500">数据库</span>
                        <span class="font-semibold text-gray-900">{{ stage.metadata.enriched.executionSummary.db_type }}</span>
                      </div>
                      <div v-if="stage.metadata.enriched.executionSummary.error_message" class="text-xs text-red-700 bg-red-50 border border-red-200 break-words whitespace-pre-wrap leading-relaxed p-2 rounded-lg">
                        {{ stage.metadata.enriched.executionSummary.error_message }}
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="stage.metadata.enriched.result"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">最终结果</span>
                    </div>
                    <div class="text-xs text-gray-700 space-y-2">
                      <div v-if="stage.metadata.enriched.result.summary" class="text-xs text-gray-900 leading-relaxed bg-gray-50 p-2 rounded-lg whitespace-pre-wrap break-words">
                        {{ stage.metadata.enriched.result.summary }}
                      </div>
                      <div v-if="stage.metadata.enriched.result.description" class="text-xs text-gray-900 leading-relaxed bg-gray-50 p-2 rounded-lg whitespace-pre-wrap break-words">
                        {{ stage.metadata.enriched.result.description }}
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="stage.metadata.enriched.finalSql"
                    class="border border-gray-200 rounded-[10px] bg-white p-3"
                  >
                    <div class="flex items-center justify-between gap-3 mb-2">
                      <span class="text-[13px] font-semibold text-gray-900">最终 SQL</span>
                    </div>
                    <pre class="bg-gray-900 whitespace-pre w-full box-border overflow-x-auto rounded-lg text-xs font-mono p-2.5 text-gray-200">{{ formatSql(stage.metadata.enriched.finalSql) }}</pre>
                  </div>
                </div>

                <div class="flex flex-wrap gap-3 text-xs text-gray-700 mt-1.5">
                  <span v-if="getStageElapsedTime(stage)">耗时：<strong class="font-semibold">{{ formatElapsedTime(getStageElapsedTime(stage)!) }}</strong></span>
                  <span v-if="stage.metadata?.rows !== undefined">行数：<strong class="font-semibold">{{ stage.metadata.rows }}</strong></span>
                  <span v-if="stage.metadata?.duration">耗时：<strong class="font-semibold">{{ stage.metadata.duration }}</strong></span>
                </div>
              </div>

              <div v-if="stage.suggestion" class="flex flex-wrap gap-2 mt-2.5">
                <Button
                  size="sm"
                  variant="ghost"
                  class="h-7 text-xs px-2.5"
                  @click="copySuggestion(stage.suggestion)"
                >
                  复制建议
                </Button>
              </div>
            </div>

            <div class="col-span-2" aria-hidden="true"></div>
          </div>
        </transition>
      </li>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onUnmounted, toRef } from 'vue';
import { Button } from '@/components/ui/button';
import {
  type SqlStageStateItem,
  type SqlStageStatus,
  getStageTitle,
  getStatusText,
  formatElapsedTime,
  hasFailedStage,
  isAllSuccess,
  isOverallSuccess,
  isOverallFailed,
  STATUS_TEXT_MAP,
} from '@/views/chat/types';
import MarkdownMessage from '@/components/shared/MessageRenderer/MarkdownMessage.vue';
import KnowledgeItemContent from './KnowledgeItemContent.vue';
import KnowledgeList from './KnowledgeList.vue';
import LlmRequestSection from './LlmRequestSection.vue';
import StageHeader from './StageHeader.vue';
import StatusIcon from '@/components/StatusIcon/index.vue';
import type { TimelineProps, TimelineEmits, MessageStatus } from './types';
import { TIMELINE_CONFIG } from './types';
import type { MessageExecutionStatus } from '@/api/types/chat';
import { formatSqlWithFix } from '@/utils/sqlFormatter';
import { useTimelineState } from './composables/useTimelineState';
import { useTimelineKnowledge } from './composables/useTimelineKnowledge';
import { useTimelineTiming } from './composables/useTimelineTiming';

const props = withDefaults(defineProps<TimelineProps>(), {
  stages: () => [],
  autoCollapse: true,
  autoCollapseDelay: TIMELINE_CONFIG.AUTO_COLLAPSE_DELAY,
  defaultCollapsed: false,
  showCollapseHeader: true,
  messageStatus: 'loading',
  finalStatus: null,
  hasSql: true,
  executionStatus: null,
  stagesFinalized: false,
  showTimeoutHint: true,
});

const emit = defineEmits<TimelineEmits>();

// 使用 composables 管理状态
const stagesRef = toRef(props, 'stages');
const hasSqlRef = toRef(props, 'hasSql');
const stagesFinalizedRef = toRef(props, 'stagesFinalized');
const timelineState = useTimelineState(
  stagesRef,
  props.defaultCollapsed,
  hasSqlRef,
  stagesFinalizedRef
);

const {
  isCollapsed,
  stageExpandStates,
  expandedKnowledgeItems,
  expandedFilteringSteps,
  expandedDetailSections,
  toggleStage,
  toggleKnowledgeItem,
  isKnowledgeItemExpanded,
  toggleFilteringStep,
  isFilteringStepExpanded,
  toggleDetailSection,
  isSectionExpanded,
  toggleCollapse: toggleCollapseState,
} = timelineState;

// 知识库相关逻辑
const knowledge = useTimelineKnowledge(stagesRef);
const {
  getKnowledgeDetails,
  getKnowledgeItemKey,
  getKnowledgeBaseLink,
  getKnowledgeTitle,
  getKnowledgeTypeClass,
  getStageToggleKey,
} = knowledge;

// 定时器相关逻辑
const timing = useTimelineTiming(stagesRef);
const {
  getStageElapsedTime,
  totalElapsedTime,
} = timing;

// 自动折叠定时器
let autoCollapseTimer: ReturnType<typeof setTimeout> | null = null;

const normalizeTimelineStatus = (status?: MessageStatus | string | null): SqlStageStatus | undefined => {
  if (!status) return undefined;
  const normalized = String(status).toLowerCase();
  if (['success', 'failed', 'processing', 'pending', 'skipped'].includes(normalized)) {
    return normalized as SqlStageStatus;
  }
  return undefined;
};

/**
 * 计算显示的阶段列表 - 直接显示所有阶段,不做过滤
 */
const displayStages = computed(() => {
  if (!props.stages || props.stages.length === 0) return [];
  return props.stages;
});

const failedStages = computed(() => props.stages.filter(stage => stage.status === 'failed'));
const hasActiveStages = computed(() =>
  props.stages.some(stage => stage.status === 'processing' || stage.status === 'pending')
);
const isTimelineFinalized = computed(() => {
  if (!props.stages || props.stages.length === 0) {
    return false;
  }

  // 如果仍有节点在进行中，则继续视为未完成
  if (hasActiveStages.value) {
    return false;
  }

  // 优先使用明确的 finalize 信号
  if (props.stagesFinalized) {
    return true;
  }

  // 兜底逻辑：如果满足以下条件也认为已完成
  // 1. 所有阶段都已完成（没有 processing 或 pending）
  // 2. 有明确的执行结果（execRes 或有效的 executionStatus）
  // 3. messageStatus 不是 loading 或 processing
  const allStagesCompleted = !hasActiveStages.value;
  const hasExecutionResult =
    props.execRes !== undefined ||
    (props.executionStatus && props.executionStatus !== 'initialization');
  const messageNotLoading =
    props.messageStatus !== 'loading' && props.messageStatus !== 'processing';

  return allStagesCompleted && hasExecutionResult && messageNotLoading;
});

const isNoSqlScenario = computed(() => {
  if (props.hasSql) return false;
  if (failedStages.value.length === 0) return false;
  return failedStages.value.every(stage => stage.key === 'sql_generation');
});

const resolvedExecutionStatus = computed<MessageExecutionStatus | null>(() => {
  if (props.executionStatus) {
    if (props.executionStatus === 'sql_failed' && props.execRes === 1 && !props.hasSql) {
      return 'no_sql';
    }
    if (props.executionStatus === 'sql_success' && !props.hasSql) {
      return 'no_sql';
    }
    return props.executionStatus;
  }

  if (props.execRes === 1) {
    return props.hasSql ? 'sql_success' : 'no_sql';
  }

  if (props.execRes === 0) {
    if (isNoSqlScenario.value) {
      return 'no_sql';
    }
    return 'sql_failed';
  }

  if (isNoSqlScenario.value) {
    return 'no_sql';
  }

  return null;
});

/**
 * 当前整体状态
 * 优先级:
 * 1. messageStatus（loading/processing）保持进行中状态
 * 2. executionStatus（细粒度执行状态）
 * 3. messageStatus / execRes / finalStatus 兜底判断
 * 4. 阶段数据分析
 */
const currentStatus = computed((): SqlStageStatus => {
  const normalizedMessageStatus = normalizeTimelineStatus(props.messageStatus);

  // 如果有正在进行的阶段，整体状态始终是 processing
  const processingStage = props.stages.find(s => s.status === 'processing');
  if (processingStage) {
    return 'processing';
  }

  // 【核心拦截】流程未完成时，始终返回 processing
  // 不管 messageStatus、executionStatus、execRes 是什么
  if (!isTimelineFinalized.value) {
    return 'processing';
  }

  // ========== 以下逻辑只在流程完成后执行 ==========

  // 使用 messageStatus 的 success/failed 状态
  if (normalizedMessageStatus === 'success' || normalizedMessageStatus === 'failed') {
    return normalizedMessageStatus;
  }

  // 使用 execRes 判断
  if (props.execRes !== undefined) {
    const result = props.execRes === 1 ? 'success' : 'failed';
    return result;
  }

  // 使用 finalStatus
  const normalizedFinalStatus = normalizeTimelineStatus(props.finalStatus ?? undefined);
  if (normalizedFinalStatus) {
    return normalizedFinalStatus;
  }

  // 流程已完成，判断最终状态
  if (isOverallSuccess(props.stages)) return 'success';
  if (isOverallFailed(props.stages)) return 'failed';

  if (hasFailedStage(props.stages)) {
    return 'failed';
  }

  if (isAllSuccess(props.stages)) {
    const hasCriticalStage = props.stages.some(s =>
      ['data_execution', 'result_return', 'cache_hit'].includes(s.key)
    );
    return hasCriticalStage ? 'success' : 'failed';
  }

  return 'pending';
});

/**
 * 当前状态文案
 */
const currentStatusBaseLabel = computed(() => {
  const status = currentStatus.value;

  // 时间线标题只显示 3 个状态：进行中、成功、失败
  // 不显示"等待中"和"跳过"

  // 【优先级1】如果是 processing 状态，直接返回"进行中"
  if (status === 'processing') {
    return getStatusText(status);  // "进行中"
  }

  // 【优先级2】如果是失败状态，返回失败信息
  if (status === 'failed') {
    // 整体时间线标签不使用具体阶段的标题，统一显示"SQL执行失败"
    // 具体的失败原因在展开的阶段详情中查看
    return 'SQL执行失败';
  }

  // 【优先级3】如果是成功状态，返回成功信息
  if (status === 'success') {
    // no_sql 场景：显示 "成功（无SQL）"
    // 有 SQL 场景：显示 "SQL执行成功"
    return props.hasSql ? 'SQL执行成功' : '成功（无SQL）';
  }

  // pending 和 skipped 状态不显示文字，返回空字符串
  return '';
});

const currentStatusText = computed(() => {
  // 直接使用 currentStatusBaseLabel，它已经包含完整的状态文本
  // 失败场景："SQL执行失败"
  // 成功场景（有SQL）："SQL执行成功"
  // 成功场景（无SQL）："成功（无SQL）"
  // 进行中场景："进行中"
  return currentStatusBaseLabel.value;
});

/**
 * 获取阶段显示序号 - 动态根据实际出现顺序编号
 */
const getStageDisplayNumber = (index: number) => {
  return index + 1;
};

/**
 * 获取状态徽章类
 */
const getStatusBadgeClass = (status: SqlStageStatus) => {
  const classMap: Record<SqlStageStatus, string> = {
    pending: 'bg-gray-100 text-gray-500 border border-gray-200',
    processing: 'bg-blue-50 text-blue-700 border border-blue-200 font-semibold animate-pulse',
    success: 'bg-green-100 text-green-800 border border-green-200 font-semibold',
    failed: 'bg-red-100 text-red-800 border border-red-200 font-semibold',
    skipped: 'bg-gray-50 text-gray-500 border border-gray-200',
  };
  return classMap[status] || 'bg-gray-100 text-gray-500 border border-gray-200';
};

/**
 * 判断阶段是否有可展开的详情
 */
const hasStageDetails = (stage: SqlStageStateItem) => {
  return !!(
    stage.description ||
    stage.errorMessage ||
    stage.suggestion ||
    (stage as SqlStageStateItem & { cacheHit?: boolean }).cacheHit ||
    (stage.metadata && Object.keys(stage.metadata).length > 0)
  );
};

/**
 * 格式化 JSON 对象为字符串
 */
const formatJson = (value: unknown): string => {
  try {
    return JSON.stringify(value, null, 2);
  } catch (err) {
    return String(value);
  }
};

/**
 * 获取 JSON 预览文本（截断长文本）
 */
const getJsonPreview = (value: unknown, maxLength = TIMELINE_CONFIG.JSON_PREVIEW_LENGTH): string => {
  const text = formatJson(value);
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}…`;
};

/**
 * 格式化值显示
 */
const formatValue = (value: unknown): string => {
  if (value === null || value === undefined) return '无';
  if (typeof value === 'object') {
    if (Array.isArray(value)) {
      return value.length ? `${value.length} 项` : '[]';
    }
    return getJsonPreview(value, TIMELINE_CONFIG.JSON_PREVIEW_SHORT_LENGTH);
  }
  if (typeof value === 'boolean') {
    return value ? '是' : '否';
  }
  return String(value);
};

/**
 * 格式化 SQL
 */
const formatSql = (sql: string): string => {
  try {
    return formatSqlWithFix(sql, {
      tabWidth: 2,
      keywordCase: 'upper',
      linesBetweenQueries: 2,
    });
  } catch (err) {
    console.error('SQL 格式化失败:', err);
    return sql;
  }
};

/**
 * 复制到剪贴板（统一处理）
 */
const copyToClipboard = async (text: string): Promise<void> => {
  try {
    await navigator.clipboard.writeText(text);
    const { toast } = await import('@/components/ui/toast');
    toast({
      title: '复制成功',
      variant: 'success'
    });
  } catch (err) {
    console.error('复制失败:', err);
    const { toast } = await import('@/components/ui/toast');
    toast({
      title: '复制失败，请重试',
      variant: 'error'
    });
  }
};

/**
 * 复制建议到剪贴板
 */
const copySuggestion = async (suggestion: string) => {
  await copyToClipboard(suggestion);
};

/**
 * 复制 JSON 对象到剪贴板
 */
const copyJson = async (data: unknown) => {
  await copyToClipboard(formatJson(data));
};

/**
 * 切换折叠状态
 */
const toggleCollapse = () => {
  toggleCollapseState();
  emit('toggle-collapse', isCollapsed.value);
};

/**
 * 格式化阶段摘要，过滤技术细节
 */
const getFormattedSummary = (stage: SqlStageStateItem): string => {
  if (!stage.summary) return '';

  // 过滤掉 backend_fallback 等技术标记
  const summary = stage.summary.trim();

  // 如果 summary 只是技术标记，不显示
  if (summary === 'backend_fallback' ||
      summary.startsWith('(backend_fallback)') ||
      summary === 'llm' ||
      summary === 'not_applicable') {
    return '';
  }

  // 直接显示后端返回的 summary，不做任何映射或组装
  return summary;
};

/**
 * 判断是否应该显示阶段描述
 */
const shouldShowStageDescription = (stage: SqlStageStateItem, index?: number): boolean => {
  if (!stage.description) return false;
  const isKnowledgeRetrieval = stage.key === 'knowledge_retrieval';
  const hasKnowledgeDetails = getKnowledgeDetails(stage, index).length > 0;
  return !(isKnowledgeRetrieval && hasKnowledgeDetails);
};

/**
 * 判断是否应该显示空描述提示
 */
const shouldShowEmptyDescription = (stage: SqlStageStateItem, index?: number): boolean => {
  const isKnowledgeRetrieval = stage.key === 'knowledge_retrieval';
  const hasKnowledgeDetails = getKnowledgeDetails(stage, index).length > 0;
  const hasEnriched = !!stage.metadata?.enriched;
  return !hasEnriched && !(isKnowledgeRetrieval && hasKnowledgeDetails);
};

/**
 * 处理自动折叠
 */
const handleAutoCollapse = () => {
  // 清除之前的定时器
  if (autoCollapseTimer) {
    clearTimeout(autoCollapseTimer);
    autoCollapseTimer = null;
  }

  // 如果开启自动折叠且流程全部成功
  if (props.autoCollapse && isTimelineFinalized.value && isOverallSuccess(props.stages)) {
    autoCollapseTimer = setTimeout(() => {
      isCollapsed.value = true;
      emit('toggle-collapse', true);
    }, props.autoCollapseDelay);
  }
};

// 监听阶段变化，处理自动折叠
watch(
  [
    () => props.stagesFinalized,
    isTimelineFinalized,
  ],
  ([finalized, timelineFinalized]) => {
    if (finalized || timelineFinalized) {
      handleAutoCollapse();
    }
  }
);

// 组件卸载时清理定时器
onUnmounted(() => {
  if (autoCollapseTimer) {
    clearTimeout(autoCollapseTimer);
    autoCollapseTimer = null;
  }
});
</script>

<style scoped>
/* Vue transition 动画 */
.fade-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  opacity: 0;
}

.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.25s ease;
}

.collapse-enter-to,
.collapse-leave-from {
  max-height: 320px;
  opacity: 1;
}

/* 状态徽章图标旋转动画 */
.icon--spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Markdown 详情样式 */
.detail-markdown {
  font-size: 12px;
  max-width: 100%;
  overflow: visible;
}

.detail-markdown :deep(.markdown-article) {
  font-size: 12px;
  line-height: 1.5;
  max-width: 100%;
}

.detail-markdown :deep(.code-block) {
  margin: 8px 0;
  font-size: 12px;
  max-width: 100%;
  overflow-x: auto;
}

.detail-markdown :deep(pre) {
  overflow-x: auto;
  max-width: 100%;
}

/* 移动端适配 - 使用深度选择器覆盖子组件样式（必须使用自定义样式） */
@media screen and (max-width: 768px) {
  /* 优化详情区域在移动端的显示 */
  .detail-markdown {
    font-size: 11px !important;
  }
  
  .detail-markdown :deep(.markdown-article) {
    font-size: 11px !important;
  }
  
  .detail-markdown :deep(.code-block) {
    font-size: 10px !important;
    margin: 6px 0 !important;
  }
}
</style>
