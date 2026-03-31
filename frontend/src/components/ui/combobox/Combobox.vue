<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { Check, ChevronsUpDown } from 'lucide-vue-next';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';

const props = defineProps<{
  options: { label: string; value: string }[];
  placeholder?: string;
  emptyMessage?: string;
  modelValue?: string;
  class?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const open = ref(false);
const inputValue = ref(props.modelValue || '');
const searchQuery = ref('');

const selectedLabel = computed(() => {
  if (!inputValue.value) return '';
  const option = props.options.find((opt) => opt.value === inputValue.value);
  return option ? option.label : inputValue.value;
});

const filteredOptions = computed(() => {
  if (!searchQuery.value) {
    return props.options;
  }

  const filtered = props.options.filter((option) =>
    option.label.toLowerCase().includes(searchQuery.value.toLowerCase())
  );

  const hasExactMatch = filtered.some(
    (option) => option.label.toLowerCase() === searchQuery.value.toLowerCase()
  );

  if (!hasExactMatch && searchQuery.value.trim()) {
    return [...filtered, { label: `创建 "${searchQuery.value}"`, value: searchQuery.value }];
  }

  return filtered;
});

watch(
  () => props.modelValue,
  (newVal) => {
    inputValue.value = newVal || '';
  }
);

const handleSelect = (value: string) => {
  inputValue.value = value;
  emit('update:modelValue', value);
  open.value = false;
  searchQuery.value = '';
};

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && searchQuery.value.trim()) {
    handleSelect(searchQuery.value);
  }
};
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        class="w-full justify-between"
        :class="props.class"
      >
        {{ selectedLabel || placeholder }}
        <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[320px] p-0" align="start" side="bottom">
      <div class="p-3 border-b">
        <Input
          :placeholder="placeholder"
          v-model="searchQuery"
          @keydown="handleKeydown"
          class="h-9"
        />
      </div>
      <div
        class="max-h-[300px] overflow-y-auto"
        style="scrollbar-width: thin; scrollbar-color: rgb(209 213 219) rgb(243 244 246);"
      >
        <div v-if="filteredOptions.length === 0" class="py-6 text-center text-sm text-muted-foreground">
          {{ emptyMessage }}
        </div>
        <div
          v-for="option in filteredOptions"
          :key="option.value"
          class="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent cursor-pointer"
          @click="handleSelect(option.value)"
        >
          <Check
            :class="cn('mr-2 h-4 w-4', inputValue === option.value ? 'opacity-100' : 'opacity-0')"
          />
          {{ option.label }}
        </div>
      </div>
    </PopoverContent>
  </Popover>
</template>
