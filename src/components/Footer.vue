<template>
  <footer
    class="w-full bg-gradient-to-br from-[#735e59] to-[#b9a994] border-t border-[#ede5dd]/20"
  >
    <!-- Seção principal do footer -->
    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-12">
      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12"
      >
        <!-- Links Rápidos -->
        <div class="space-y-4">
          <h3
            class="text-xl font-semibold text-[#ede5dd] font-['Prata',serif] mb-6 relative"
          >
            Links Rápidos
            <div
              class="absolute -bottom-2 left-0 w-12 h-0.5 bg-gradient-to-r from-[#ede5dd] to-transparent rounded-full"
            ></div>
          </h3>
          <nav class="space-y-3">
            <a
              href="/"
              class="group flex items-center text-[#ede5dd]/80 hover:text-[#ede5dd] transition-all duration-300 hover:translate-x-1"
            >
              <i
                class="fa-solid fa-home mr-3 text-sm group-hover:text-[#ede5dd] transition-colors duration-300"
              ></i>
              <span class="relative">
                Home
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#ede5dd] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
            <a
              href="/produtos"
              class="group flex items-center text-[#ede5dd]/80 hover:text-[#ede5dd] transition-all duration-300 hover:translate-x-1"
            >
              <i
                class="fa-solid fa-box mr-3 text-sm group-hover:text-[#ede5dd] transition-colors duration-300"
              ></i>
              <span class="relative">
                Produtos
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#ede5dd] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
            <a
              href="/trocas-devolucoes"
              class="group flex items-center text-[#ede5dd]/80 hover:text-[#ede5dd] transition-all duration-300 hover:translate-x-1"
            >
              <i
                class="fa-solid fa-refresh mr-3 text-sm group-hover:text-[#ede5dd] transition-colors duration-300"
              ></i>
              <span class="relative">
                Trocas & Devoluções
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#ede5dd] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
            <a
              href="/cuidados"
              class="group flex items-center text-[#ede5dd]/80 hover:text-[#ede5dd] transition-all duration-300 hover:translate-x-1"
            >
              <i
                class="fa-solid fa-heart mr-3 text-sm group-hover:text-[#ede5dd] transition-colors duration-300"
              ></i>
              <span class="relative">
                Cuidados
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#ede5dd] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
          </nav>
        </div>

        <!-- Meios de Pagamento -->
        <div class="space-y-4">
          <h3
            class="text-xl font-semibold text-[#ede5dd] font-['Prata',serif] mb-6 relative"
          >
            Meios de Pagamento
            <div
              class="absolute -bottom-2 left-0 w-12 h-0.5 bg-gradient-to-r from-[#ede5dd] to-transparent rounded-full"
            ></div>
          </h3>
          <div class="space-y-3">
            <div
              class="flex items-center space-x-3 p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-[#ede5dd]/20 hover:bg-white/20 transition-all duration-300"
            >
              <div
                class="w-8 h-8 bg-[#ede5dd] rounded-md flex items-center justify-center"
              >
                <i class="fa-solid fa-qrcode text-[#735e59] text-sm"></i>
              </div>
              <span class="text-[#ede5dd] font-medium">PIX</span>
            </div>
          </div>
        </div>

        <!-- Formas de Envio -->
        <div class="space-y-4">
          <h3
            class="text-xl font-semibold text-[#ede5dd] font-['Prata',serif] mb-6 relative"
          >
            Formas de Envio
            <div
              class="absolute -bottom-2 left-0 w-12 h-0.5 bg-gradient-to-r from-[#ede5dd] to-transparent rounded-full"
            ></div>
          </h3>
          <div class="space-y-3">
            <div
              class="flex items-center space-x-3 p-3 bg-white/10 backdrop-blur-sm rounded-lg border border-[#ede5dd]/20 hover:bg-white/20 transition-all duration-300"
            >
              <div
                class="w-8 h-8 bg-[#ede5dd] rounded-md flex items-center justify-center"
              >
                <i class="fa-solid fa-truck text-[#735e59] text-sm"></i>
              </div>
              <span class="text-[#ede5dd] font-medium">Correios</span>
            </div>
          </div>
        </div>

        <!-- Contatos -->
        <div class="space-y-4">
          <h3
            class="text-xl font-semibold text-[#ede5dd] font-['Prata',serif] mb-6 relative"
          >
            Contatos
            <div
              class="absolute -bottom-2 left-0 w-12 h-0.5 bg-gradient-to-r from-[#ede5dd] to-transparent rounded-full"
            ></div>
          </h3>
          <div class="space-y-3">
            <a
              target="_blank"
              href="https://wa.me/5554994112420?text=Ol%C3%A1,%20vim%20pelo%20site%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es"
              class="group flex items-center space-x-3 p-3 bg-green-600/20 backdrop-blur-sm rounded-lg border border-green-400/30 hover:bg-green-600/30 transition-all duration-300 hover:scale-105"
            >
              <div
                class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center group-hover:bg-green-400 transition-colors duration-300"
              >
                <i class="fa-brands fa-whatsapp text-white text-sm"></i>
              </div>
              <div class="flex flex-col">
                <span class="text-[#ede5dd] font-medium text-sm">WhatsApp</span>
                <span class="text-[#ede5dd]/80 text-xs">+55 54 9411-2420</span>
              </div>
            </a>

            <a
              target="_blank"
              href="https://www.instagram.com/luyka_pratas/"
              class="group flex items-center space-x-3 p-3 bg-gradient-to-r from-purple-600/20 to-pink-600/20 backdrop-blur-sm rounded-lg border border-purple-400/30 hover:from-purple-600/30 hover:to-pink-600/30 transition-all duration-300 hover:scale-105"
            >
              <div
                class="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center group-hover:from-purple-400 group-hover:to-pink-400 transition-all duration-300"
              >
                <i class="fa-brands fa-instagram text-white text-sm"></i>
              </div>
              <div class="flex flex-col">
                <span class="text-[#ede5dd] font-medium text-sm"
                  >Instagram</span
                >
                <span class="text-[#ede5dd]/80 text-xs">@luyka_pratas</span>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Seção de copyright -->
    <div class="border-t border-[#ede5dd]/20 bg-black/20 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-6">
        <div
          class="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0"
        >
          <div class="text-center md:text-left">
            <p class="text-[#ede5dd]/80 text-sm">
              © 2025 LUYKA - CNPJ: 61.835.152/0001-07
            </p>
            <p class="text-[#ede5dd]/60 text-xs mt-1">
              Todos os direitos reservados.
            </p>
          </div>

          <div class="flex items-center space-x-2 text-[#ede5dd]/60 text-sm">
            <span>Desenvolvido com</span>
            <i class="fa-solid fa-heart text-red-400 animate-pulse"></i>
            <span>por</span>
            <a
              target="_blank"
              href="https://www.instagram.com/edu_morbecks/"
              class="text-[#ede5dd] hover:text-[#ede5dd]/80 transition-colors duration-300 font-medium"
            >
              @edu_morbecks
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
