<script setup lang="ts">
import type { CheckboxRootEmits, CheckboxRootProps } from 'radix-vue'
import type { HTMLAttributes } from 'vue'
import { Check, Minus } from 'lucide-vue-next'
import { CheckboxIndicator, CheckboxRoot, useForwardPropsEmits } from 'radix-vue'
import { cn } from '@/lib/utils'
import { computed, toRefs } from 'vue'

interface Props extends CheckboxRootProps {
  class?: HTMLAttributes['class']
  indeterminate?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  indeterminate: false
})

const emits = defineEmits<CheckboxRootEmits>()

// 手动实现 reactiveOmit 的功能 - 创建一个计算属性来排除特定属性
const delegatedProps = computed(() => {
  const { class: _, indeterminate: __, ...rest } = props
  return rest
})

const forwarded = useForwardPropsEmits(delegatedProps, emits)

// 计算状态
const checkboxState = computed(() => {
  if (props.indeterminate) return 'indeterminate'
  return props.checked ? 'checked' : 'unchecked'
})
</script>

<template>
  <CheckboxRoot
    v-bind="forwarded"
    :data-state="checkboxState"
    :class="
      cn('peer h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground data-[state=indeterminate]:bg-primary data-[state=indeterminate]:text-primary-foreground',
         props.class)"
  >
    <CheckboxIndicator class="flex h-full w-full items-center justify-center text-current">
      <slot>
        <Check v-if="!indeterminate" class="h-4 w-4" />
        <Minus v-else class="h-4 w-4" />
      </slot>
    </CheckboxIndicator>
  </CheckboxRoot>
</template>
