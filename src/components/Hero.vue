<template>
  <section
    class="w-full h-[calc(100vh-5rem)] max-h-screen relative overflow-hidden mt-20"
  >
    <div
      class="absolute inset-0"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
    >
      <div
        ref="carouselRef"
        class="flex h-full"
        :class="{
          'transition-transform duration-1000 ease-in-out': !isDragging,
        }"
        :style="{
          transform: `translateX(calc(-${
            currentIndex * 100
          }% + ${touchOffset}px))`,
        }"
      >
        <div
          v-for="(slide, idx) in slides"
          :key="idx"
          class="min-w-full h-full relative bg-gradient-to-br from-[#ede5dd] to-[#f5f0ea]"
          :style="{
            backgroundImage: slide.img
              ? `url(${slide.img})`
              : 'linear-gradient(135deg, #ede5dd 0%, #f5f0ea 100%)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
          }"
        >
          <div
            class="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/60"
          ></div>
          <div
            class="absolute inset-0 bg-gradient-to-r from-black/60 via-transparent to-black/60"
          ></div>
        </div>
      </div>
    </div>

    <div
      class="relative z-10 h-full flex flex-col items-center justify-center px-6 lg:px-8"
    >
      <div class="max-w-4xl mx-auto text-center">
        <div
          class="inline-flex items-center justify-center mb-6 lg:mb-8 animate-fade-in"
        >
          <div
            class="h-[1px] bg-gradient-to-r from-transparent via-white/60 to-transparent w-20 lg:w-32"
          ></div>
          <i
            class="fa-solid fa-gem mx-6 text-2xl lg:text-3xl text-white/90 drop-shadow-lg"
          ></i>
          <div
            class="h-[1px] bg-gradient-to-r from-transparent via-white/60 to-transparent w-20 lg:w-32"
          ></div>
        </div>

        <p
          class="text-lg lg:text-xl xl:text-2xl text-white/95 font-light tracking-wide leading-relaxed mb-8 lg:mb-10 max-w-2xl mx-auto drop-shadow-lg animate-fade-in-delay"
          style="
            text-shadow: 1px 1px 10px rgba(0, 0, 0, 0.5);
            font-family: 'Georgia', serif;
          "
        >
          Joias em Prata 925
        </p>
        <p
          class="text-sm lg:text-base xl:text-lg text-white/85 font-light tracking-wider uppercase letter-spacing-wider max-w-xl mx-auto drop-shadow-md animate-fade-in-delay-2"
          style="
            text-shadow: 1px 1px 8px rgba(0, 0, 0, 0.5);
            letter-spacing: 0.2em;
          "
        >
          Elegância Atemporal · Qualidade Excepcional
        </p>

        <div class="mt-10 lg:mt-12 animate-fade-in-delay-3">
          <button
            @click="goToProducts"
            class="px-8 lg:px-12 py-3 lg:py-4 bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/30 text-white text-sm lg:text-base tracking-wider uppercase transition-all duration-300 hover:scale-105 hover:shadow-xl rounded-none cursor-pointer"
            style="letter-spacing: 0.15em; font-family: 'Prata', serif"
          >
            Explorar Coleção
          </button>
        </div>
      </div>
    </div>

    <button
      @click="previousSlide"
      class="hidden lg:flex absolute left-8 top-1/2 -translate-y-1/2 z-20 w-16 h-16 rounded-full bg-white/10 hover:bg-white/20 backdrop-blur-md shadow-lg border border-white/20 items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-2xl group cursor-pointer"
      aria-label="Slide anterior"
    >
      <i
        class="fa-solid fa-chevron-left text-white text-2xl group-hover:text-white/90 transition-colors duration-300"
      ></i>
    </button>

    <button
      @click="nextSlide"
      class="hidden lg:flex absolute right-8 top-1/2 -translate-y-1/2 z-20 w-16 h-16 rounded-full bg-white/10 hover:bg-white/20 backdrop-blur-md shadow-lg border border-white/20 items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-2xl group cursor-pointer"
      aria-label="Próximo slide"
    >
      <i
        class="fa-solid fa-chevron-right text-white text-2xl group-hover:text-white/90 transition-colors duration-300"
      ></i>
    </button>

    <div
      class="absolute bottom-8 lg:bottom-12 left-1/2 -translate-x-1/2 z-20 flex gap-3"
    >
      <button
        v-for="(slide, idx) in slides"
        :key="idx"
        @click="goToSlide(idx)"
        class="transition-all duration-300 rounded-full cursor-pointer"
        :class="
          currentIndex === idx
            ? 'w-10 h-1.5 bg-white shadow-lg'
            : 'w-1.5 h-1.5 bg-white/50 hover:bg-white/70'
        "
        :aria-label="`Ir para slide ${idx + 1}`"
      ></button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const slides = [
  { img: "/1.png", alt: "Banner 1" },
  { img: "/2.png", alt: "Banner 2" },
  { img: "/3.png", alt: "Banner 3" },
];

const currentIndex = ref(0);
const touchOffset = ref(0);
const touchStartX = ref(0);
const touchStartY = ref(0);
const isDragging = ref(false);
const carouselRef = ref(null);
let autoplayInterval = null;

const goToProducts = () => {
  router.push({ name: "produtos" });
};

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % slides.length;
};

const previousSlide = () => {
  currentIndex.value =
    currentIndex.value === 0 ? slides.length - 1 : currentIndex.value - 1;
};

const goToSlide = (index) => {
  currentIndex.value = index;
};

const handleTouchStart = (e) => {
  stopAutoplay();
  isDragging.value = true;
  touchStartX.value = e.touches[0].clientX;
  touchStartY.value = e.touches[0].clientY;
  touchOffset.value = 0;
};

const handleTouchMove = (e) => {
  if (!isDragging.value) return;

  const touchCurrentX = e.touches[0].clientX;
  const touchCurrentY = e.touches[0].clientY;
  const deltaX = touchCurrentX - touchStartX.value;
  const deltaY = touchCurrentY - touchStartY.value;

  if (Math.abs(deltaX) > Math.abs(deltaY)) {
    e.preventDefault();
    touchOffset.value = deltaX;
  }
};

const handleTouchEnd = () => {
  if (!isDragging.value) return;

  const threshold = 50;

  if (Math.abs(touchOffset.value) > threshold) {
    if (touchOffset.value > 0) {
      previousSlide();
    } else {
      nextSlide();
    }
  }

  touchOffset.value = 0;
  isDragging.value = false;
  startAutoplay();
};

const startAutoplay = () => {
  autoplayInterval = setInterval(() => {
    nextSlide();
  }, 5000);
};

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval);
    autoplayInterval = null;
  }
};

onMounted(() => {
  startAutoplay();
});

onUnmounted(() => {
  stopAutoplay();
});
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}

.animate-slide-up {
  animation: slide-up 1.2s ease-out;
}

.animate-fade-in-delay {
  animation: fade-in 1.4s ease-out;
  animation-delay: 0.3s;
  animation-fill-mode: both;
}

.animate-fade-in-delay-2 {
  animation: fade-in 1.4s ease-out;
  animation-delay: 0.6s;
  animation-fill-mode: both;
}

.animate-fade-in-delay-3 {
  animation: fade-in 1.4s ease-out;
  animation-delay: 0.9s;
  animation-fill-mode: both;
}
</style>
