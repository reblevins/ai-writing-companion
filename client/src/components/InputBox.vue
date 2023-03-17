<template>
  <div v-bind="$attrs" :class="{ 'border border-gray-600 ': !editable }"
    class="w-full h-44 outline-none">
    <div class="h-full w-full focus:ring focus:ring-purple-500 outline-none p-4 overflow-auto"
      ref="textbox" contenteditable
      @input="$emit('update:modelValue', $event.target.innerText)"
      @blur="makeNormal">
        <p v-for="line in props.modelValue" :key="line">{{ line }}</p>
      </div>
  </div>
</template>

<script setup>
import { ref,defineProps, defineEmits } from "vue";

const props = defineProps({
  placeholder: String,
  modelValue: Array
});

const emit = defineEmits(["update:modelValue"])

const editable = ref(false);
const textbox = ref();
const inputText = ref(props.placeholder);

function makeEditable() {
  editable.value = true;
  setTimeout(() => {
    (textbox.value).focus()
  }, 100);
  inputText.value = props.modelValue || ""
}

function makeNormal() {
  editable.value = false;
  inputText.value = props.modelValue == "" ? props.placeholder : props.modelValue
}
</script>