<template>
  <section
    class="w-full bg-gradient-to-br from-[#735e59] to-[#b9a994] relative overflow-hidden"
  >
    <div class="absolute inset-0 opacity-10">
      <div
        class="absolute top-0 left-1/4 w-32 h-32 bg-[#ede5dd] rounded-full blur-2xl"
      ></div>
      <div
        class="absolute bottom-0 right-1/4 w-40 h-40 bg-[#b9a994] rounded-full blur-2xl"
      ></div>
      <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-[#ede5dd] rounded-full blur-xl"
      ></div>
    </div>

    <div class="absolute inset-0 opacity-5">
      <div
        class="absolute inset-0"
        style="
          background-image: radial-gradient(
            circle at 1px 1px,
            rgba(237, 229, 221, 0.3) 1px,
            transparent 0
          );
          background-size: 20px 20px;
        "
      ></div>
    </div>

    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-8 relative z-10">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
        <div
          class="group text-center transform transition-all duration-700 hover:-translate-y-2 animate-fade-in-up cursor-pointer"
          style="animation-delay: 100ms"
        >
          <div class="relative">
            <div
              class="relative inline-flex items-center justify-center w-16 h-16 mb-4 mx-auto"
            >
              <div
                class="absolute inset-0 bg-[#ede5dd]/20 rounded-full blur-lg group-hover:blur-xl transition-all duration-500"
              ></div>
              <div
                class="relative w-12 h-12 bg-gradient-to-br from-[#ede5dd] to-white rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-500 group-hover:scale-110"
              >
                <i
                  class="fa-solid fa-gem text-lg text-[#735e59] group-hover:rotate-12 transition-transform duration-500"
                ></i>
              </div>
              <div
                class="absolute inset-0 rounded-full border-2 border-[#ede5dd]/30 animate-ping group-hover:border-[#ede5dd]/50"
              ></div>
            </div>

            <div class="space-y-2">
              <h3
                class="text-lg lg:text-xl font-bold text-[#ede5dd] font-['Prata',serif] tracking-wide group-hover:text-white transition-colors duration-300"
              >
                JOIAS EM PRATA 925
              </h3>
              <p
                class="text-sm text-[#ede5dd]/80 leading-relaxed group-hover:text-[#ede5dd] transition-colors duration-300 max-w-xs mx-auto"
              >
                Autêntico, sofisticado e atemporal.
              </p>
            </div>

            <div class="mt-4 flex justify-center">
              <div
                class="w-12 h-0.5 bg-gradient-to-r from-transparent via-[#ede5dd]/50 to-transparent group-hover:w-20 group-hover:via-[#ede5dd] transition-all duration-500"
              ></div>
            </div>
          </div>
        </div>

        <div
          class="group text-center transform transition-all duration-700 hover:-translate-y-2 animate-fade-in-up"
          style="animation-delay: 300ms"
        >
          <div class="relative">
            <div
              class="relative inline-flex items-center justify-center w-16 h-16 mb-4 mx-auto"
            >
              <div
                class="absolute inset-0 bg-[#ede5dd]/20 rounded-full blur-lg group-hover:blur-xl transition-all duration-500"
              ></div>
              <div
                class="relative w-12 h-12 bg-gradient-to-br from-[#ede5dd] to-white rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-500 group-hover:scale-110"
              >
                <i
                  class="fa-solid fa-star text-lg text-[#735e59] group-hover:scale-125 transition-transform duration-500"
                ></i>
              </div>
              <div
                class="absolute inset-0 rounded-full border-2 border-[#ede5dd]/30 animate-ping group-hover:border-[#ede5dd]/50"
                style="animation-delay: 0.5s"
              ></div>
            </div>

            <div class="space-y-2">
              <h3
                class="text-lg lg:text-xl font-bold text-[#ede5dd] font-['Prata',serif] tracking-wide group-hover:text-white transition-colors duration-300"
              >
                DESCUBRA SEU BRILHO
              </h3>
              <p
                class="text-sm text-[#ede5dd]/80 leading-relaxed group-hover:text-[#ede5dd] transition-colors duration-300 max-w-xs mx-auto"
              >
                Luyka é mais do que uma marca, é uma experiência única.
              </p>
            </div>

            <div class="mt-4 flex justify-center">
              <div
                class="w-12 h-0.5 bg-gradient-to-r from-transparent via-[#ede5dd]/50 to-transparent group-hover:w-20 group-hover:via-[#ede5dd] transition-all duration-500"
              ></div>
            </div>
          </div>
        </div>

        <div
          class="group text-center transform transition-all duration-700 hover:-translate-y-2 animate-fade-in-up"
          style="animation-delay: 500ms"
        >
          <div class="relative">
            <div
              class="relative inline-flex items-center justify-center w-16 h-16 mb-4 mx-auto"
            >
              <div
                class="absolute inset-0 bg-[#ede5dd]/20 rounded-full blur-lg group-hover:blur-xl transition-all duration-500"
              ></div>
              <div
                class="relative w-12 h-12 bg-gradient-to-br from-[#ede5dd] to-white rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-500 group-hover:scale-110"
              >
                <i
                  class="fa-solid fa-shipping-fast text-lg text-[#735e59] group-hover:translate-x-1 transition-transform duration-500"
                ></i>
              </div>
              <div
                class="absolute inset-0 rounded-full border-2 border-[#ede5dd]/30 animate-ping group-hover:border-[#ede5dd]/50"
                style="animation-delay: 1s"
              ></div>
            </div>

            <div class="space-y-2">
              <h3
                class="text-lg lg:text-xl font-bold text-[#ede5dd] font-['Prata',serif] tracking-wide group-hover:text-white transition-colors duration-300"
              >
                ENVIO SEGURO
              </h3>
              <p
                class="text-sm text-[#ede5dd]/80 leading-relaxed group-hover:text-[#ede5dd] transition-colors duration-300 max-w-xs mx-auto"
              >
                Entrega rápida e segura em todo o Brasil.
              </p>
            </div>

            <div class="mt-4 flex justify-center">
              <div
                class="w-12 h-0.5 bg-gradient-to-r from-transparent via-[#ede5dd]/50 to-transparent group-hover:w-20 group-hover:via-[#ede5dd] transition-all duration-500"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out forwards;
}

@keyframes pulse-soft {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.animate-pulse {
  animation: pulse-soft 2s ease-in-out infinite;
}

@keyframes ping-custom {
  75%,
  100% {
    transform: scale(1.2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping-custom 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.group:hover .fa-gem {
  animation: gem-sparkle 0.6s ease-in-out;
}

@keyframes gem-sparkle {
  0%,
  100% {
    transform: rotate(0deg) scale(1);
  }
  25% {
    transform: rotate(6deg) scale(1.1);
  }
  75% {
    transform: rotate(-6deg) scale(1.1);
  }
}

.group:hover .fa-star {
  animation: star-glow 1.2s ease-in-out;
}

@keyframes star-glow {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.group:hover .fa-shipping-fast {
  animation: shipping-move 0.6s ease-in-out;
}

@keyframes shipping-move {
  0%,
  100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(4px);
  }
}

@media (max-width: 768px) {
  .text-lg {
    font-size: 1rem;
  }

  .lg\:text-xl {
    font-size: 1.125rem;
  }

  .group:hover {
    transform: translateY(-4px);
  }

  .w-16 {
    width: 3rem;
  }

  .h-16 {
    height: 3rem;
  }

  .w-12 {
    width: 2.5rem;
  }

  .h-12 {
    height: 2.5rem;
  }
}

@media (hover: none) {
  .group:active {
    transform: scale(0.98);
  }

  .group:active .relative {
    transform: scale(1.05);
  }
}

@keyframes pattern-float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-2px);
  }
}

.absolute.inset-0[style*="background-image"] {
  animation: pattern-float 6s ease-in-out infinite;
}
</style>
