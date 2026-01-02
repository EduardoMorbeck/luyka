<template>
  <Transition name="notification">
    <div
      v-if="visible"
      :class="[
        'max-w-md rounded-xl shadow-2xl p-4 border-2 transform transition-all duration-300',
        colorClasses,
      ]"
    >
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 mt-0.5">
          <i
            :class="[
              'text-xl',
              type === 'success'
                ? 'fa-solid fa-check-circle'
                : 'fa-solid fa-exclamation-circle',
            ]"
          ></i>
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="font-bold text-base mb-1">{{ title }}</h3>
          <p class="text-sm leading-relaxed whitespace-pre-line">
            {{ description }}
          </p>
        </div>
        <button
          @click="close"
          class="flex-shrink-0 ml-2 hover:opacity-70 transition-opacity duration-200 cursor-pointer"
        >
          <i class="fa-solid fa-times text-lg"></i>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: "success", // 'success' ou 'error'
    validator: (value) => ["success", "error"].includes(value),
  },
  duration: {
    type: Number,
    default: 5000, // 5 segundos por padrão
  },
});

const emit = defineEmits(["close"]);

const visible = ref(false);
let timeoutId = null;

const colorClasses = computed(() => {
  if (props.type === "success") {
    return "bg-green-50 border-green-200 text-green-800";
  } else {
    return "bg-red-50 border-red-200 text-red-800";
  }
});

function close() {
  visible.value = false;
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
  setTimeout(() => {
    emit("close");
  }, 300); // Aguarda a animação de saída
}

function show() {
  visible.value = true;
  if (props.duration > 0) {
    timeoutId = setTimeout(() => {
      close();
    }, props.duration);
  }
}

onMounted(() => {
  show();
});

watch(
  () => props.title,
  () => {
    if (visible.value) {
      show();
    }
  }
);

defineExpose({
  show,
  close,
});
</script>

<style scoped>
.notification-enter-active {
  transition: all 0.3s ease-out;
}

.notification-leave-active {
  transition: all 0.3s ease-in;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%) translateY(20px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%) translateY(20px);
}

.notification-enter-to,
.notification-leave-from {
  opacity: 1;
  transform: translateX(0) translateY(0);
}
</style>
