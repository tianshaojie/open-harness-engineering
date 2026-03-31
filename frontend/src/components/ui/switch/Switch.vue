<script setup lang="ts">
import type { SwitchRootEmits, SwitchRootProps } from 'radix-vue'
import type { HTMLAttributes } from 'vue'
import { SwitchRoot, SwitchThumb, useForwardPropsEmits } from 'radix-vue'
import { cn } from '@/lib/utils'
import { computed } from 'vue'

interface Props extends SwitchRootProps {
  class?: HTMLAttributes['class']
}

const props = withDefaults(defineProps<Props>(), {})

const emits = defineEmits<SwitchRootEmits>()

// 手动实现 reactiveOmit 的功能 - 创建一个计算属性来排除特定属性
const delegatedProps = computed(() => {
  const { class: _, ...rest } = props
  return rest
})

const forwarded = useForwardPropsEmits(delegatedProps, emits)
</script>

<template>
  <SwitchRoot
    v-bind="forwarded"
    :class="
      cn('peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-input',
         props.class)"
  >
    <SwitchThumb
      :class="
        cn('pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0')
      "
    />
  </SwitchRoot>
</template> 